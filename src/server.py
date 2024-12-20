import sys
import os
from fuzzywuzzy import process, fuzz
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from pyngrok import ngrok
from pyngrok import conf
from models.round import AggregateLayout, Round, group_comparable_rounds
from util.configuration import load_config_into_env
from util.database import Database
from enum import Enum
from waitress import serve
from logger import logger

app = Flask(__name__, static_folder='../site/build', static_url_path='/')
CORS(app)

class ErrorCode(Enum):
    SUCCESS = 0
    ERROR_NO_MATCHES = 1
    ERROR_NO_LAYOUTS = 2
    ERROR_NO_ROUNDS = 3

@app.route('/', methods=['GET'])
def home():
    logger.info("Loaded home page")
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/rating/<course_name>/<layout_name>/<score>', methods=['GET'])
def rating(course_name: str, layout_name: str, score: str):
    db = Database(os.getenv("db_connection"))
    score_int = int(score)
    all_course_names = [course.readable_course_name for course in db.query_courses()]
    scored_course_names: tuple[str, int] = process.extractBests(
        course_name, 
        all_course_names, 
        scorer=fuzz.partial_ratio, 
        score_cutoff=0, 
        limit=5)
    
    logger.info("Scored course names: " + str(scored_course_names))

    # ERROR: No close course matches
    if len(scored_course_names) == 0:
        logger.info(f"Failed to calculate rating for {score} at [{course_name}: {layout_name}] - no close course matches")
        db.close()
        return jsonify({
            "status": ErrorCode.ERROR_NO_MATCHES.value,
            "close_courses": [],
        }), 200
    
    if course_name.lower() in [course.lower() for course in all_course_names]:
        chosen_course_name = course_name
    else:
        chosen_course_name = scored_course_names[0][0]    
    rounds = db.query_rounds_for_course(chosen_course_name)
    all_layout_names = set([round.layout_name for round in rounds])

    matching_layout_scores = process.extractBests(
        layout_name, 
        all_layout_names, 
        scorer=fuzz.token_set_ratio, 
        score_cutoff=50, 
        limit=100)    

    # ERROR: No close layout matches
    if len(matching_layout_scores) == 0:
        logger.info(f"Failed to calculate rating for {score} at [{course_name}: {layout_name}] - no close layout matches")
        db.close()
        return jsonify({
            "status": ErrorCode.ERROR_NO_LAYOUTS.value,
            "close_layouts": list(all_layout_names)[:10],
        }), 200
    
    matching_layout_names = [layout for layout, _ in matching_layout_scores]
    matching_rounds = [round for round in rounds if round.layout_name in matching_layout_names]
    
    # ERROR: No rounds for layout
    if len(matching_rounds) == 0:
        logger.info(f"Failed to calculate rating for {score} at [{course_name}: {layout_name}] - no rounds for layout")
        db.close()
        return jsonify({
            "status": ErrorCode.ERROR_NO_ROUNDS.value,
            "close_layouts": matching_layout_names,
        }), 200
    
    grouped_layouts = group_comparable_rounds(matching_rounds)
    if len(grouped_layouts) == 0:
        logger.info(f"Failed to calculate rating for {score} at [{course_name}: {layout_name}] - layouts could not be grouped")
        db.close()
        return jsonify({}), 200

    chosen_layout = grouped_layouts[0]
    score_rating = chosen_layout.score_rating(score_int)['rating']
    logger.info(f"Rated {score} at [{course_name}: {layout_name}] - {score_rating}")
    db.close()
    return jsonify(build_success_data()), 200

@app.route('/api/courses', methods=['GET'])
def courses():
    db = Database(os.getenv("db_connection"))
    courses = db.query_courses()
    db.close()
    return jsonify([course.readable_course_name for course in courses])

@app.route('/api/layouts/<course_name>', methods=['GET'])
def layouts(course_name: str):
    db = Database(os.getenv("db_connection"))
    rounds = db.query_rounds_for_course(course_name)
    layout_names = list(set([round.layout_name for round in rounds]))
    db.close()
    return jsonify(layout_names)

def build_success_data(course_name: str, layout_name: str, score: int, rating: int, layout: AggregateLayout, rounds: list[Round]) -> dict:
    return {
        "course_name": course_name,
        "layout_name": layout_name,
        "score": score,
        "score_rating": rating,
        "layout": {
            "layout_hole_distances": [
            {
                "hole_number": num+1,
                "distance": dist
            }
            for num, dist in enumerate(layout.layout_hole_distances)],
            "layout_total_distance": layout.layout_total_distance,
            "layout_par": layout.layout_par,
            "layouts": layout.layouts_to_url(),
        },
        "rounds": [
            {
                "round_date": 0,
                "num_rounds": 0,
                "round_rating": 0,
            }
        ],
        "percentile": 0
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 server.py <config_file>")
        sys.exit(1)

    config_file_path = sys.argv[1]
    load_config_into_env(config_file_path)
    serve(app, host='0.0.0.0', port=80)
