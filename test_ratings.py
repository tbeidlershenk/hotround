from scrape_events import get_all_sanctioned_events
from scrape_ratings import get_round_ratings_for_tournament
import json
from logger import logger

course_names = {
    "DV_Top_Gun_SlasherplusAction": "DV Top Gun (Slasher+Action)",
    "Eagles_Landing_DG_course": "Eagles Landing DG course",
    "Evergreen_Park_AB": "Evergreen Park",
}
course_events = {
    course: {
        'events': get_all_sanctioned_events(course)
    } for course in list(course_names.keys())
}
with open('test/course_events.json', 'w') as f:
    json.dump(course_events, f, indent=4)
logger.info('Events fetched and dumped to course_events.json.')
logger.info('')

logger.info('Fetching ratings...')
with open('test/course_events.json') as f:
    course_events: dict = json.load(f)
course_ratings = {}
for course in course_events:
    events = course_events[course]['events']
    course_ratings[course] = {
        event: get_round_ratings_for_tournament(event) for event in events
    }
with open('test/course_ratings.json', 'w') as f:
    json.dump(course_ratings, f, indent=4)
logger.info('Ratings fetched and dumped to course_ratings.json.')
logger.info('')

logger.info('Compiling data...')
with open('test/course_events.json') as f:
    course_events: dict = json.load(f)
with open('test/course_ratings.json') as f:
    course_ratings: dict = json.load(f)
course_data = {
    course: {
        'name': course_names[course],
        'events': course_events[course],
        'ratings': course_ratings[course]
    } for course in course_names
}
with open('test/course_data.json', 'w') as f:
    json.dump(course_data, f, indent=4)
logger.info('Data compiled and dumped to course_data.json.')
logger.info('')
