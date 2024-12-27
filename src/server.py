from datetime import datetime
import json
from pickle import NONE
import sys
import os
from fuzzywuzzy import process, fuzz
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from pyngrok import ngrok
from pyngrok import conf
from exts import status
from models.round import Layout, Round, AggregateLayout, Round, group_comparable_rounds
from util.configuration import load_config_into_env
from util.database import Database
from enum import Enum
from waitress import serve
from logger import logger

app = Flask(__name__, static_folder='../site/build', static_url_path='/')
CORS(app)

status_none = -1
status_success = 0
status_error_no_matches = 1
status_error_no_layouts = 2
status_error_no_rounds = 3

@app.route('/', methods=['GET'])
def home():
    logger.info("Loaded home page")
    return send_from_directory(app.static_folder, 'index.html')

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
    layouts = group_comparable_rounds(rounds)
    data = [{
        "layout_tokens": layout.layout_tokens,
        "layout_names": layout.layout_names,
        "layout_hole_distances": layout.layout_hole_distances,
        "layout_total_distance": layout.layout_total_distance,
        "layout_par": layout.layout_par,
    } for layout in layouts]
    db.close()
    return jsonify(data), 200

@app.route('/api/rating/<course_name>', methods=['GET'])
def new_rating(course_name: str):
    db = Database(os.getenv("db_connection"))
    rounds = db.query_rounds_for_course(course_name)
    layouts = group_comparable_rounds(rounds)
    db.close()
    return jsonify(build_success_data(
        course_name=course_name, 
        layouts=layouts
    )), 200
    
def build_success_data(course_name: str, layouts: list[Layout]) -> dict:
    return [
        {
            "status": status_success,
            "course_name": course_name,
            "layout_name": layout.get_descriptive_name(),
            "layout_hole_distances": [
                {
                    "hole_number": num+1,
                    "distance": dist
                }
                for num, dist in enumerate(layout.layout_hole_distances)],
            "layout_total_distance": layout.layout_total_distance,
            "layout_par": layout.layout_par,
            "num_holes": layout.num_holes,
            "par_rating": layout.par_rating,
            "stroke_value": layout.stroke_value,
            "layouts": layout.layouts_to_url(),
            "rounds": [
                {
                    "round_date": "2021-01-01",
                    "num_rounds": 0,
                    "round_rating": 0,
                }
                for round in layout.rounds_used],
            "percentile": 0
        }
        for layout in layouts]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 server.py <config_file>")
        sys.exit(1)

    config_file_path = sys.argv[1]
    load_config_into_env(config_file_path)
    if os.getenv("debug") == "True":
        app.run(host='0.0.0.0', port=80)
    else:
        serve(app, host='0.0.0.0', port=80)
