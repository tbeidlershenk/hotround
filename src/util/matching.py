from models.course import Course

def course_name_contains_tokens(course: Course, tokens: list[str]) -> bool:
    course_name_tokens = course.get_name_tokens()
    for x in tokens:
        if x.lower() not in course_name_tokens:
            return False
    return True

def get_similar_course_names(course: Course, num_courses: int = 5) -> list[str]:
    pass