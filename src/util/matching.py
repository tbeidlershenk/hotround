from models.course import Course
from itertools import groupby
from collections import Counter

def course_name_contains_tokens(course: Course, tokens: list[str]) -> bool:
    course_name_tokens = course.get_name_tokens()
    for x in tokens:
        if x.lower() not in course_name_tokens:
            return False
    return True

def get_similar_course_names(course: Course, num_courses: int = 5) -> list[str]:
    pass

def filter_duplicates(courses: list[Course]) -> list[Course]:
    counts = Counter([c.get_name() + c.get_location() for c in courses])
    filtered_courses = []
    for c in courses:
        name_loc = c.get_name() + c.get_location()
        if counts[name_loc] == 1:
            filtered_courses.append(c)
        elif c.has_events():
            filtered_courses.append(c)
        else:
            pass
        
    return filtered_courses
            
