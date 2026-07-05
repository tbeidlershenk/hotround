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
import shutil

if len(sys.argv) == 2:
    config_file_path = sys.argv[1]
    load_config_into_env(config_file_path)

db_path = os.getenv("db_path")
db_file_name = os.getenv("db_file_name")
db_path_full = db_path + db_file_name

if not os.path.exists(db_path_full):
    logger.info(f"Database file not found at {db_path_full}.")
    exit(1)

connection = os.getenv("db_connection")
database = Database(connection=connection)
scraper = Scraper()

# 1. scrape locations from dgscene
locations = scraper.get_locations_dgscene()

# 2. scrape courses for each location
#    merge back to db, updates course details
# for i, location in enumerate(locations):
#     logger.info(f"{i+1}/{len(locations)} - {location}")
#     courses = scraper.get_courses_dgscene(location)
#     for course in courses:
#         database.merge_data(course)
#     logger.info(f"Courses Found - {len(courses)}")
#     logger.info("")
        
courses = database.query_courses()

# 3. scrape events for each course
#    pull from current year
#    skip events already scraped
#    skip events in the future
for i, course in enumerate(courses):
    logger.info(f"{i+1}/{len(courses)} - {course.get_name()}")
    events = scraper.get_events_dgscene(course.course_id)
    for event in events:
        event_exists = database.event_exists(event.event_id)
        event_has_rounds = database.event_contains_round_data(event.event_id)
        if event_exists and event_has_rounds:
            logger.info(f"Skip  - {event.event_id}: event already exists in database")
            continue
        rounds = scraper.get_ratings_pdgalive(event.event_id)
        logger.info(f"Fetch - {event.event_id}")
        database.merge_data(course=course, events=events, rounds=rounds)
    logger.info(f"Events Found - {len(events)}")
    logger.info("")


