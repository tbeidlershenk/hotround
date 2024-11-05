# 1. Import and install requirements
from logger import logger
from util.database import Database
from util.scraper import Scraper
import json
import chromedriver_autoinstaller
import time
from time import sleep
from tqdm import tqdm

# Load configuration
with open('scraper_config.json') as f:
    config: dict = json.load(f)
    
database = Database(connection=config['db_connection'])
scraper = Scraper(chromedriver_path=config['chromedriver_path'])

chromedriver_autoinstaller.install()

# 4. Fetch ratings for each event and load into DB
try:
    logger.info('Fetching ratings...')
    start_time = time.time()

    if config['courses_json'] is not None:
        with open(config['courses_json']) as f:
            course_names: dict = json.load(f)
    else:
        course_names = {x.course_name : x.readable_course_name for x in database.query_all_courses()}

    if config['events_json'] is not None:
        with open(config['events_json']) as f:
            course_events: dict = json.load(f)
    else:
        course_events = [scraper.get_all_sanctioned_events(x, config['events_start']) for x in course_names.keys()]

    for i, course in enumerate(course_events):
        progress = f'{i+1}/{len(course_events)}'
        elapsed_time = time.time() - start_time
        elapsed_time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        est_time_remaining = elapsed_time / (i + 1) * (len(course_events) - i)
        est_time_str = f'{int(est_time_remaining // 3600):02}:{time.strftime("%M:%S", time.gmtime(est_time_remaining % 3600))}'
        logger.info(f'Elapsed time: {elapsed_time_str} seconds, progress: {progress}, est. time remaining: {est_time_str}')

        events = course_events[course]
        rounds = []

        for j, event in enumerate(events):
            event_id = event['event_id']
            if database.event_exists(event_id):
                logger.info(f'Skipping {event_id} (already scraped)...')
                continue

            course_ratings = scraper.get_round_ratings_for_tournament(event_id)
            rounds.extend(course_ratings)
            logger.info(f'Event {j+1}/{len(events)} - Course {i+1}/{len(course_events)}')

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