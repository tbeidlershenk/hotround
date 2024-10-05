from fuzzywuzzy import process, fuzz
import time


def is_match(str1: str, str2: str) -> bool:
    str1 = str1.replace('_', ' ')
    str2 = str2.replace('_', ' ')
    return fuzz.partial_ratio(str1, str2) == 100


def get_matching_courses(search_term: str) -> dict[str, int]:
    before = time.time()
    with open('all_courses.txt', 'r') as file:
        all_courses = [line.strip() for line in file.readlines()]
    after = time.time()
    print(after-before)
    all_courses = [x.replace('_', ' ') for x in all_courses]

    partial_ratio_matches = process.extract(search_term, all_courses,
                                            scorer=fuzz.partial_ratio, limit=50)
    token_sort_ratio_matches = process.extract(search_term, all_courses,
                                               scorer=fuzz.token_sort_ratio, limit=50)
    matches = {}
    for match in partial_ratio_matches[0:5] + token_sort_ratio_matches[0:5]:
        print(type(match))
        name = match[0]
        score = match[1]
        print(name)
        print(score)
        if name not in matches.keys():
            matches[name] = score
        else:
            matches[name] = max(matches[name], score)

    print(
        '\n'.join([f'{name}: {matches[name]}' for name in matches.keys()]))


get_matching_courses('Moraine State Park')
