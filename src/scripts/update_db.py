from datetime import datetime
import os
import time
from util.database import Database
from util.scraper import Scraper
from logger import logger

def run_update(db_connection: str, num_workers: int, chromedriver_path: str, rescrape_events=True, after_date: datetime = None):
    db_path = 'data/pdga_data.db'

    # Get all courses
    logger.info('Running update script...')
    database = Database(connection=db_connection)
    scraper = Scraper(chromedriver_path=chromedriver_path)
    courses = database.query_courses()

    # Get all events (no after_date)
    if rescrape_events:
        logger.info('Rescraping events...')
        try:
            all_events = []
            start_time = time.time()
            for i, course in enumerate(courses):
                course_name = course.course_name
                logger.info(f'Fetching events for {course.readable_course_name}...')
                events = scraper.get_all_sanctioned_events(course_name, after_date=after_date)
                all_events.extend(events)
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
        events = all_events
    else:
        logger.info('Pulling events from database...')
        events = database.query_events()

    # Remove events already in db
    logger.info('Filtering out events already in database...')
    events = [event for event in events if not database.event_exists(event.event_id)]

    # Split remaining events into n groups
    logger.info(f'Splitting {len(events)} events into {num_workers} groups...')
    split_events = [events[i::num_workers] for i in range(num_workers)]

    # Build the image
    logger.info('Building docker image...')
    os.system(f'docker build -t round-rating-scraper -f Dockerfile.webscraper .')

    # Spin up n docker containers
    logger.info(f'Spinning up {num_workers} docker containers...')
    for i, events in enumerate(split_events):
        event_ids = [event.event_id for event in events]
        event_ids_str = ','.join([str(event_id) for event_id in event_ids])
        os.system(f'docker run -d --name scraper_{i} -e EVENT_IDS={event_ids_str} -e DB_CONNECTION={db_connection} -v {db_path}:/app/data.db round-rating-scraper')
    
    logger.info('Done.')