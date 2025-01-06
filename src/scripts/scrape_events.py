import warnings
warnings.filterwarnings("ignore")

from util.database import Database
from util.scraper import Scraper
from logger import logger
from datetime import datetime
import json
import time

def scrape_events(config: dict, after_date: datetime = None):
    database = Database(connection=config['db_connection'])
    scraper = Scraper(chromedriver_path=config['chromedriver_path'])

    try:
        logger.info("Scraping events...")
        start_time = time.time()
        courses = database.query_courses_with_no_events()

        after_date = datetime.strptime(config['after_date'], '%Y-%m-%d')
        for i, course in enumerate(courses):
            course_name = course.course_name
            logger.info(f'Fetching events for {course.readable_course_name}...')

            events = scraper.get_all_sanctioned_events(course_name, after_date=after_date)
            database.merge_events(events=events)

            progress = f'{i+1}/{len(courses)}'
            percentage = f'{(float(i+1) / len(courses) * 100):.2f}%'
            elapsed_time = time.time() - start_time
            elapsed_time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
            logger.info(f'Progress: {progress} = {percentage}, Elapsed time: {elapsed_time_str} seconds')
            logger.info("")

    except BaseException as e:
        logger.info(f'Error fetching events: {e}')
    except KeyboardInterrupt as e:
        logger.info(f'Error fetching events: {e}')

    scraper.cleanup()
    logger.info("Exiting...")

