from datetime import datetime
import time
import warnings
warnings.filterwarnings("ignore")

import os
from logger import logger
from util.database import Database
from util.scraper import Scraper

logger.info("Starting scraper...")
event_ids_str = os.getenv('EVENT_IDS')
event_ids = [int(event_id) for event_id in event_ids_str.split(',')]
logger.info(f"Scraping {len(event_ids)}.")

db_connection = os.getenv('DB_CONNECTION')
scraper = Scraper(chromedriver_path='/usr/bin/chromedriver')
logger.info(f"Built scraper")

try:
    logger.info("Scraping ratings...")
    start_time = time.time()
    courses = Database(connection=db_connection).query_courses()
    num_events = len(event_ids)

    for i, event_id in enumerate(event_ids):
        logger.info(f'Fetching ratings for {event_id}...')

        if Database(connection=db_connection).event_contains_round_data(event_id):
            logger.info(f'Skipping {event_id} (already scraped)...')
            continue

        rounds = scraper.get_round_ratings_for_tournament(event_id)
        # if rounds == []:
        #     logger.info(f'No ratings scraped from {event_id}, removing from database.')
        #     Database(connection=db_connection).delete_event(event_id)
        #     continue

        Database(connection=db_connection).merge_rounds(rounds)
        logger.info(f'Done fetching ratings for {event_id}.')

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
logger.info("Exiting...")