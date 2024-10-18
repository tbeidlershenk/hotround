import json
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import numpy as np
from util import depluralize

with open('data/course_ratings.json', 'r') as file:
    course_ratings = json.load(file)

with open('data/course_names.json', 'r') as file:
    course_names = json.load(file)

course_search_terms = 'Cranbrook'
layout_search_terms = 'Longs'

best_match_course = process.extractOne(
    course_search_terms, course_names.values())
best_match_key = next(key for key, value in course_names.items()
                      if value == best_match_course[0])

print(
    f"Best match for course '{course_search_terms}': {best_match_course[0]} (Key: {best_match_key})")

course_name = course_names[best_match_key]
course_data: dict = course_ratings[best_match_key]
# Compile all rounds for each tournament ID together
all_rounds = []
for _, rounds in course_data.items():
    all_rounds.extend(rounds)

# Rank each layout based on the search terms
layout_search_results = []
for round_data in all_rounds:
    layout_name: str = round_data['course_layout']
    # Use a different matching criteria: partial ratio
    # De-pluralize the search term and layout name tokens
    search_tokens = [depluralize(x) for x in layout_search_terms.split()]
    layout_name_tokens = [depluralize(x) for x in layout_name.split()]

    match_score = sum(
        process.extractOne(token, layout_name_tokens,
                           scorer=fuzz.partial_ratio)[1]
        for token in search_tokens
    ) / len(search_tokens)

    layout_search_results.append((round_data, match_score))

# Sort the results by match score in descending order
layout_search_results.sort(key=lambda x: x[1], reverse=True)

# Print the ranked layouts
print(f"Ranked layouts for search term '{layout_search_terms}':")
for round_data, score in layout_search_results:
    print(f"Layout: {round_data['course_layout']}, Score: {score}")


def remove_outliers(data, m=2):
    mean = np.mean(data)
    std_dev = np.std(data)
    print(std_dev)
    return [x for x in data if abs(x - mean) < m * std_dev]


# Filter rounds with more than a certain number of players
min_players = 4
# Define a threshold for layout match score
match_score_threshold = 70
layout_search_results = [x[0]
                         for x in layout_search_results if x[1] > match_score_threshold]

# Extract ratings
ratings = [round_data['par_rating'] for round_data in layout_search_results]

# Remove outliers
ratings = remove_outliers(ratings)

# Calculate average rating and standard deviation
average_rating = np.mean(ratings)
std_dev_rating = np.std(ratings)

print(
    f"Average rating for rounds with more than {min_players} players: {average_rating}")
print(f"Standard deviation of ratings: {std_dev_rating}")
