import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
import io
from flask import Flask, jsonify, send_from_directory, send_file
from flask_cors import CORS
from util.configuration import load_config_into_env, verify_config
from util.database import Database
from waitress import serve
from logger import logger
from collections import Counter

app = Flask(__name__, static_folder="../site/build", static_url_path="/")
CORS(app)

status_none = -1
status_success = 0
status_error_no_matches = 1
status_error_no_layouts = 2
status_error_no_rounds = 3


@app.route("/", methods=["GET"])
def home():
    logger.info("Loaded home page")
    return send_from_directory(app.static_folder, "index.html")

@app.route("/courses.txt")
def courses_txt():
    db = Database(os.getenv("db_connection"))
    courses = db.query_courses()
    db.close()
    name_counts = Counter([c.get_name() for c in courses])
    lines = []
    for c in courses:
        name = c.get_name()
        loc = c.get_location()
        lines.append(f"{name} ({loc})" if name_counts[name] > 1 else name)
    lines = list(set(lines))
    lines.sort()
    content = '\n'.join(lines)
    file_content = io.BytesIO(content.encode('utf-8'))
    file_content.seek(0)
    return send_file(file_content, mimetype='text/plain', download_name='courses.txt')

@app.route("/api/status", methods=["GET"])
def status():
    logger.info("Uptime status check")
    return jsonify({"online": True})


@app.route("/api/courses", methods=["GET"])
def courses():
    db = Database(os.getenv("db_connection"))
    courses = db.query_courses()
    db.close()
    return jsonify([course.get_name() for course in courses])

@app.route("/api/rating/<course_name>", methods=["GET"])
def rating(course_name: str):
    db = Database(os.getenv("db_connection"))
    courses = db.query_courses()
    course = [x for x in courses if x.get_name() == course_name][0]
    aggregated_layouts = db.query_aggregate_layouts(course.course_id)
    db.close()

    # TODO not sure if this is the best way to filter out weird data
    returned_layouts = [x for x in aggregated_layouts if x.num_rounds >= 5]
    num_results = len(returned_layouts)
    logger.info(f"Generated {num_results} layouts for {course_name}")

    if num_results == 0:
        return jsonify({
            "status": status_error_no_matches,
            "course_name": course_name,
            "num_results": 0,
            "layouts": [],
        }), 200

    return jsonify({
        "status": status_success,
        "course_name": course_name,
        "num_results": num_results,
        "layouts": [x.to_dict() for x in returned_layouts],
    }), 200
    


if __name__ == "__main__":
    if len(sys.argv) == 2:
        config_file_path = sys.argv[1]
        load_config_into_env(config_file_path)

    db_path = os.getenv("db_path")
    db_file_name = os.getenv("db_file_name")
    port = os.getenv("PORT")

    if not os.path.exists(db_path + db_file_name):
        raise ValueError(f"No db file at path: {db_path + db_file_name}.")

    serve(app, host="0.0.0.0", port=port)
