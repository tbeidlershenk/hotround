import logging
import sys
from fuzzywuzzy import process, fuzz
import os
from flask import Flask, jsonify
from flask_cors import CORS
from pyngrok import ngrok
from pyngrok import conf
from models.round import group_comparable_rounds
from util.configuration import load_config_into_env
from util.database import Database
from enum import Enum
from waitress import serve
from logger import logger

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all routes and origins

class ErrorCode(Enum):
    SUCCESS = 0
    ERROR_NO_MATCHES = 1
    ERROR_NO_LAYOUTS = 2
    ERROR_NO_ROUNDS = 3

@app.route('/', methods=['GET'])
def home():
    return jsonify(message="Online", status=200)

@app.route('/rating/<course_name>/<layout_name>/<score>', methods=['GET'])
def get_rating(course_name: str, layout_name: str, score: str):
    score_int = int(score)
    all_course_names = [course.readable_course_name for course in db.query_courses()]
    scored_course_names: tuple[str, int] = process.extractBests(
        course_name, 
        all_course_names, 
        scorer=fuzz.token_set_ratio, 
        score_cutoff=0, 
        limit=5)

    # ERROR: No close course matches
    if course_name.lower() not in [course.lower() for course, _ in scored_course_names]:
        similar_course_names = [course for course, _ in scored_course_names]
        logger.info(f"Failed to calculate rating for {score} at [{course_name}: {layout_name}] - no close course matches")
        return jsonify({
            "status": ErrorCode.ERROR_NO_MATCHES.value,
            "close_courses": similar_course_names[:5],
        }), 200
    
    rounds = db.query_rounds_for_course(course_name)
    all_layout_names = set([round.layout_name for round in rounds])
    scored_layouts: tuple[str, int] = process.extractBests(
        layout_name, 
        all_layout_names, 
        scorer=fuzz.token_set_ratio, 
        score_cutoff=0, 
        limit=10)

    # ERROR: No close layout matches
    if len(scored_layouts) == 0:
        similar_layout_names = [layout for layout, _ in scored_layouts]
        logger.info(f"Failed to calculate rating for {score} at [{course_name}: {layout_name}] - no close layout matches")
        return jsonify({
            "status": ErrorCode.ERROR_NO_LAYOUTS.value,
            "close_layouts": similar_layout_names[:5],
        }), 200

    matching_layout_names = [layout for layout, _ in process.extractBests(
        layout_name, 
        all_layout_names, 
        scorer=fuzz.partial_token_sort_ratio, 
        score_cutoff=75, 
        limit=100)]
    matching_rounds = [round for round in rounds if round.layout_name in matching_layout_names]
    # if len(matching_rounds) == 0:
    #     similar_layout_names = [layout for layout, _ in scored_layouts]
    #     logger.info(f"Failed to calculate rating for {score} at [{course_name}: {layout_name}] - no close layout matches")
    #     return jsonify({
    #         "status": ErrorCode.ERROR_NO_LAYOUTS.value,
    #         "close_layouts": similar_layout_names[:5],
    #     }), 200
    
    grouped_layouts = group_comparable_rounds(matching_rounds)
    chosen_layout = grouped_layouts[0]
    score_rating = chosen_layout.score_rating(score_int)['rating']
    logger.info(f"Calculated rating for {score} at [{course_name}: {layout_name}] - {score_rating}")
    return jsonify({
        "status": ErrorCode.SUCCESS.value,
        "score_rating": score_rating,
        "layout": chosen_layout.to_dict(),
    }), 200

def configure_logging():
    app.logger.setLevel(logging.CRITICAL+1)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.CRITICAL+1)

def run_server():
    port = int(os.getenv("flask_port"))
    ngrok_config = os.getenv("ngrok_config")
    if ngrok_config != None:   
        configure_logging()     
        conf.get_default().config_path = ngrok_config
        ngrok.connect(addr=port, name="caddiebot")
        serve(app, port=port)
    else:
        serve(app, port=port)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 server.py <config_file>")
        sys.exit(1)

    config_file_path = sys.argv[1]
    load_config_into_env(config_file_path)
    db = Database(os.getenv("db_connection"))
    run_server()