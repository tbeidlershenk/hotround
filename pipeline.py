from scrape_courses import get_courses_from_dgscene, get_readable_course_name
from scrape_events import get_all_sanctioned_events
from scrape_ratings import get_round_ratings_for_tournament
import json
from logger import logger

# TODO
# generate list of all courses
# write to json
# {
#     "course_id": "course_name"
# }
# logger.info('Fetching courses...')
# courses = get_courses_from_dgscene()
# course_names = {
#     course: get_readable_course_name(course) for course in courses
# }
# with open('data/course_names.json', 'w') as f:
#     json.dump(course_names, f, indent=4)
# logger.info('Courses fetched and dumped to courses.json.')
# logger.info('')

# TODO
# run get_all_sanctioned_events for each course
# generate dictionary of course -> event ids
# write to json
# {
#     "course_id": {
#         "events": [event_id]
#     }
# }
# logger.info('Fetching events...')
# with open('data/course_names.json') as f:
#     course_names: dict = json.load(f)
# course_events = {}
# for i, course in enumerate(course_names):
#     logger.info(f'Fetching event {i}/{len(course_names)}')
#     course_events[course] = get_all_sanctioned_events(course)
# with open('data/course_events.json', 'w') as f:
#     json.dump(course_events, f, indent=4)
# logger.info('Events fetched and dumped to course_events.json.')
# logger.info('')

# TODO
# run get_round_ratings_for_tournament for each event
# generate dictionary of course -> event ids -> round ratings
# write to json
# {
#     "course_id": {
#         "events": {
#             "event_id": {
#                 "layout": {
#                     "round": 1,
#                     "players": 25,
#                     "high_rating": 1000,
#                     "low_rating": 900,
#                     "stroke_value": 10.0,
#                     "par_rating": 950
#                 }
#             }
#         }
#     }
# }
try:
    logger.info('Fetching ratings...')
    with open('data/course_events.json') as f:
        course_events: dict = json.load(f)
    with open('data/course_ratings.json') as f:
        course_ratings: dict = json.load(f)

    for i, course in enumerate(course_events):
        if course in course_ratings:
            logger.info(f'Skipping {course} (already scraped)...')
            continue
        course_ratings[course] = {}
        events = course_events[course]

        for j, event in enumerate(events):
            course_ratings[course][event] = get_round_ratings_for_tournament(
                event)
            logger.info(
                f'Event {j+1}/{len(events)} - Course {i+1}/{len(course_events)}')

        # periodically save ratings to file
        with open('data/course_ratings.json', 'w') as f:
            json.dump(course_ratings, f, indent=4)

except BaseException as e:
    logger.info(f'Error fetching ratings: {e}')
except KeyboardInterrupt as e:
    logger.info(f'Error fetching ratings: {e}')

# with open('data/course_ratings.json', 'w') as f:
#     json.dump(course_ratings, f, indent=4)
# logger.info('Ratings dumped to course_ratings.json.')
# logger.info('')

# TODO
# create one dictionary for all data
# write to json
# logger.info('Compiling data...')
# with open('data/course_names.json') as f:
#     course_names: dict = json.load(f)
# with open('data/course_events.json') as f:
#     course_events: dict = json.load(f)
# with open('data/course_ratings.json') as f:
#     course_ratings: dict = json.load(f)
# course_data = {
#     course: {
#         'name': course_names[course],
#         'events': course_events[course],
#         'ratings': course_ratings[course]
#     } for course in course_names
# }
# with open('data/course_data.json', 'w') as f:
#     json.dump(course_data, f, indent=4)
# logger.info('Data compiled and dumped to course_data.json.')
# logger.info('')

# TODO
# setup DB schema
# develop script to insert into DB
