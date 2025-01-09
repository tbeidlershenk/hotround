import warnings
warnings.filterwarnings("ignore")
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

from models.round import Round
from util.database import Database
from util.scraper import Scraper
import json
import time
from logger import logger
from datetime import datetime

def scrape_ratings(config: dict):
    database = Database(connection=config['db_connection'])
    scraper = Scraper()

    try:
        logger.info("Scraping ratings...")
        start_time = time.time()
        courses = database.query_courses()
        num_events = len(database.query_events())
        events = database.query_events_with_no_rounds()
        num_events = len(events)
        failing_events = []

        for i, event in enumerate(events):
            event_id = event.event_id
            course = [course for course in courses if course.course_name == event.course_name][0]
            logger.info(f'Fetching ratings for {event_id} at {course.readable_course_name}...')

            if database.event_contains_round_data(event_id):
                logger.info(f'Skipping {event_id} (already scraped)...')
                continue

            rounds = scraper.get_round_ratings_for_tournament(event_id)
            if rounds == []:
                logger.info(f'No ratings scraped from {event_id}, removing from database.')
                database.delete_event(event_id)
                failing_events.append(event_id)
                continue

            database.merge_rounds(rounds)
            logger.info(f'Done fetching ratings for {event_id} at {course.readable_course_name}.')

            progress = f'{i+1}/{num_events}'
            percentage = f'{(float(i+1) / num_events * 100):.2f}%'
            elapsed_time = time.time() - start_time
            elapsed_time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
            logger.info(f'Progress: {progress} = {percentage}, Elapsed time: {elapsed_time_str} seconds')
            logger.info("")

    except BaseException as e:
        logger.info(f'Error fetching ratings: {e}')
    except KeyboardInterrupt as e:
        logger.info(f'Error fetching ratings: {e}')

    scraper.cleanup()
    # curr_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # with open(f'data/failing_events_{curr_time}.json', 'w') as f:
    #     json.dump(failing_events, f)
    logger.info("Exiting...")