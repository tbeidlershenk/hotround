# 1. Import and install requirements
from logger import logger
from util.database import Database
from util.scraper import Scraper
import json
import itertools
import chromedriver_autoinstaller

database = Database("sqlite:///data/pdga_data.db")
scraper = Scraper()

chromedriver_autoinstaller.install()

# 4. Fetch ratings for each event and load into DB
try:
    logger.info('Fetching ratings...')
    
    with open('data/course_names.json') as f:
        course_names: dict = json.load(f)
    with open('data/course_events.json') as f:
        course_events: dict = json.load(f)
    
    for i, course in enumerate(course_events):
        events = course_events[course]
        if len(events) == 0:
            logger.info(f'Skipping {course} (no events found)...')
            continue

        rounds = []

        for j, event in enumerate(events):
            event_id = event['event_id']
            if database.event_exists(event_id):
                logger.info(f'Skipping {event_id} (already scraped)...')
                continue

            course_ratings = scraper.get_round_ratings_for_tournament(event_id)
            rounds.extend(course_ratings)
            logger.info(f'Event {j+1}/{len(events)} - Course {i+1}/{len(course_events)}')

        if len(rounds) == 0:
            logger.info(f'Skipping {course} (no new rounds found)...')
            continue

        data = {
            'course_name': course,
            'readable_course_name': course_names[course],
            'events': course_events[course],
            'rounds': rounds
        }
        database.insert_course_data(data)
        

except BaseException as e:
    logger.info(f'Error fetching ratings: {e.with_traceback()}')
except KeyboardInterrupt as e:
    logger.info(f'Error fetching ratings: {e.with_traceback()}')

scraper.cleanup()
logger.info("Done")