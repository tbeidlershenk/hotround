import json
import itertools
from logger import logger
from util import is_match


def drop_rounds_from_other_courses(source_json: str, target_json: str) -> None:
    with open(source_json, 'r') as f:
        source_data = json.load(f)

    # removes the rounds for each course that aren't related to that course (ie. Knob Hill round under a Moraine tournament)
    # compare "readable course name" with "course name" in the round data
    for course in source_data:
        course_name: str = source_data[course]['name']
        events: dict[int, list] = source_data[course]['events']
        rounds: list[dict] = itertools.chain.from_iterable(events.values())
        filtered_rounds = [x for x in rounds if is_match(
            course_name, x['course'])]

    with open(target_json, 'w') as f:
        json.dump(source_data, f, indent=4)


def dry_run_drop_rounds_from_other_courses(source_json: str, target_json: str) -> None:
    with open(source_json, 'r') as f:
        source_data = json.load(f)

    # removes the rounds for each course that aren't related to that course (ie. Knob Hill round under a Moraine tournament)
    # compare "readable course name" with "course name" in the round data
    for course in source_data:
        course_name: str = source_data[course]['name']
        events: dict[int, list] = source_data[course]['events']
        rounds: list[dict] = itertools.chain.from_iterable(events.values())
        for round in rounds:
            if is_match(course_name, round['course']):
                logger.info(
                    f'Pass: {course_name} == {round["course"]}')
            else:
                logger.info(
                    f'Fail: {course_name} != {round["course"]}')
        filtered_rounds = [x for x in rounds if is_match(
            course_name, x['course'])]


def remove_invalid_rounds(source_json: str, target_json: str) -> None:
    with open(source_json, 'r') as f:
        source_data = json.load(f)

    # removes rounds that have a stroke value of 0 or less

    with open(target_json, 'w') as f:
        json.dump(source_data, f, indent=4)
