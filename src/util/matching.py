

def course_name_contains_tokens(course_name: str, tokens: list[str]):
    course_name_tokens = course_name.lower().split(' ')
    for x in tokens:
        if x.lower() not in course_name_tokens:
            return False
    return True