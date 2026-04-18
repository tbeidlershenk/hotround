import warnings

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
        if database.event_exists(event.event_id):
            logger.info(f"Skip  - {event.event_id}: event already exists in database")
            continue
        rounds = scraper.get_round_ratings_for_tournament(event.event_id)
        database.merge_data(course=course, events=events, rounds=rounds)

    logger.info(f"Done.")
    logger.info("")

# after_date = database.query_most_recent_event_date("Deer_Lakes_Park")
# events = scraper.get_all_sanctioned_events(
#     "Deer_Lakes_Park", after_date=datetime.now() - timedelta(days=14)
# )

# for event in events:
#     print(event.event_id)
#     rounds = scraper.get_round_ratings_for_tournament(event.event_id)
#     print(len(rounds))

# rounds = scraper.get_round_ratings_for_tournament(100112)
# print(len(rounds))
# for round in rounds:
#     print(round.par_rating)
