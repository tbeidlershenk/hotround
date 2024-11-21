import logging
from fuzzywuzzy import process, fuzz
import os
from flask import Flask, jsonify
from pyngrok import ngrok
from pyngrok import conf

from models.round import group_comparable_rounds
from util.database import Database
from enum import Enum

app = Flask(__name__)
db = Database(os.getenv("db_connection"))

class ErrorCode(Enum):
    SUCCESS = 0
    ERROR_NO_MATCHES = 1
    ERROR_NO_LAYOUTS = 2
    ERROR_NO_ROUNDS = 3

@app.route('/', methods=['GET'])
def home():
    return jsonify(message="Online", status=200)

@app.route('/rating/<str:course_name>/<str:layout_name>/<int:score>', methods=['GET'])
def get_rating(course_name: str, layout_name: str, score: int):
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
        return jsonify({
            "title": f"No matches for course '{course_name}'.",
            "status": ErrorCode.ERROR_NO_MATCHES,
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
        return jsonify({
            "title": f"No PDGA tournaments found for '{course_name}'.",
            "status": ErrorCode.ERROR_NO_LAYOUTS,
            "close_layouts": similar_layout_names[:5],
        }), 200

    matching_layout_names = [layout for layout, _ in process.extractBests(
        layout_name, 
        all_layout_names, 
        scorer=fuzz.partial_token_sort_ratio, 
        score_cutoff=75, 
        limit=100)]
    matching_rounds = [round for round in rounds if round.layout_name in matching_layout_names]
    grouped_layouts = group_comparable_rounds(matching_rounds)
    chosen_layout = grouped_layouts[0]
    return jsonify({
        "status": ErrorCode.SUCCESS,
        "rounds": matching_rounds,
        "score_rating": chosen_layout.score_rating(score),
        "layout": chosen_layout.to_dict(),
    }), 200

    

def configure_logging():
    app.logger.setLevel(logging.CRITICAL+1)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.CRITICAL+1)

def run_server():
    ngrok_config = os.getenv("ngrok_config")
    if ngrok_config is None:
        return
    configure_logging()
    port = int(os.getenv("flask_port"))
    conf.get_default().config_path = ngrok_config
    ngrok.connect(addr=port, name="caddiebot")
    app.run(port=port)
