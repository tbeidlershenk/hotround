import sys
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from line_profiler import profile
from util.configuration import load_config_into_env
from util.database import Database
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

@app.route('/api/rating/<course_name>', methods=['GET'])
def rating(course_name: str):
    db = Database(os.getenv("db_connection"))
    aggregated_layouts = db.query_aggregate_layouts(course_name)
    num_results = len(aggregated_layouts)
    if num_results == 0:
        db.close()
        return jsonify({
            "status": status_error_no_matches,
            "course_name": course_name,
            "num_results": 0,
            "layouts": []
        }), 200
    
    db.close()
    return jsonify({
        "status": status_success,
        "course_name": course_name,
        "num_results": num_results,
        "layouts": [x.to_dict() for x in aggregated_layouts]
    }), 200
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 server.py <config_file>")
        sys.exit(1)

    config_file_path = sys.argv[1]
    load_config_into_env(config_file_path)
    if os.getenv("debug") == "True":
        app.run(host='0.0.0.0', port=5001)
    else:
        serve(app, host='0.0.0.0', port=5001)
