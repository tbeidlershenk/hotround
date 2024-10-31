from fuzzywuzzy import fuzz

def is_match(str1: str, str2: str, threshold: int = 55) -> tuple[bool, int]:
    str1 = str1.replace('_', ' ')
    str2 = str2.replace('_', ' ')
    score = fuzz.partial_ratio(str1, str2)
    return score >= threshold, score


def depluralize(word: str) -> str:
    return word[:-1] if word.endswith('s') else word