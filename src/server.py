import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import json
import sys
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from util.configuration import build_kaggle_config, load_config_into_env, verify_config
from util.database import Database
from waitress import serve
from logger import logger
from kaggle.api.kaggle_api_extended import KaggleApi

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

@app.route('/api/rating/<course_name>', methods=['GET'])
def rating(course_name: str):
    db = Database(os.getenv("db_connection"))
    aggregated_layouts = db.query_aggregate_layouts(course_name)
    db.close()

    # TODO not sure if this is the best way to filter out weird data
    returned_layouts = [x for x in aggregated_layouts if x.num_rounds >= 10]
    num_results = len(returned_layouts)
    logger.info(f"Generated {num_results} layouts for {course_name}")
    
    if num_results == 0:
        return jsonify({
            "status": status_error_no_matches,
            "course_name": course_name,
            "num_results": 0,
            "layouts": []
        }), 200
    
    return jsonify({
        "status": status_success,
        "course_name": course_name,
        "num_results": num_results,
        "layouts": [x.to_dict() for x in returned_layouts]
    }), 200
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        config_file_path = sys.argv[1]
        load_config_into_env(config_file_path)
    verify_config(["db_location", "db_connection", "kaggle_username", "kaggle_key"])

    logger.info("Connecting to Kaggle...")
    build_kaggle_config()
    api = KaggleApi()
    api.authenticate()
    path = os.getenv("db_location")
    api.dataset_download_files(
        dataset='tobiasbeidlershenk/pdga-sanctioned-disc-golf-tournament-data', 
        path=path, 
        unzip=True)
    if not os.path.exists(path + '/pdga_data.db'):
        raise ValueError("Failed to download Kaggle dataset.")
    logger.info("Downloaded Kaggle dataset.")

    if os.getenv("debug") == "True":
        app.run(host='0.0.0.0', port=80)
    else:
        serve(app, host='0.0.0.0', port=80)
