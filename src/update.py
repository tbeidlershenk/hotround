import warnings

from util.kaggle import pull_from_kaggle, push_to_kaggle

warnings.filterwarnings("ignore")

from util.configuration import load_config_into_env
from util.database import Database
from util.scraper import Scraper
from logger import logger
from datetime import datetime, timedelta
import json
import time
import sys
import os

if len(sys.argv) == 2:
    config_file_path = sys.argv[1]
    load_config_into_env(config_file_path)

db_path = os.getenv("db_path")
db_file_name = os.getenv("db_file_name")

if not os.path.exists(db_path + db_file_name):
    logger.info(
        f"Database file not found at {db_path + db_file_name}. Pulling from Kaggle..."
    )
    exit(1)
    pull_from_kaggle()

connection = os.getenv("db_connection")
database = Database(connection=connection)
scraper = Scraper()

courses = database.query_courses()

for i, course in enumerate(courses):
    logger.info(
        f"{i+1}/{len(courses)}: Updating events for {course.readable_course_name}..."
    )
    events = scraper.get_all_sanctioned_events(course.course_name, year=2025)
    for event in events:
        event_exists = database.event_exists(event.event_id)
        event_has_rounds = database.event_contains_round_data(event.event_id)
        if event_exists and event_has_rounds:
            logger.info(f"Skip  - {event.event_id}: event already exists in database")
            continue
        rounds = scraper.get_round_ratings_for_tournament(event.event_id)
        database.merge_data(course=course, events=events, rounds=rounds)

    logger.info(f"Done.")
    logger.info("")

# push_to_kaggle()
