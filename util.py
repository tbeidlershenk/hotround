from typing import Tuple
import requests
from logger import logger
import time
from fuzzywuzzy import fuzz


def get_request_avoid_rate_limit(url: str, sleep_time: int = 60) -> requests.Response:
    """
    Makes a GET request to the specified URL and handles rate limiting by retrying after a specified sleep time.
    Args:
        url (str): The URL to send the GET request to.
        sleep_time (int, optional): The time to wait (in seconds) before retrying the request if rate limited. Defaults to 60 seconds.
    Returns:
        requests.Response: The response object from the GET request.
    Raises:
        requests.exceptions.HTTPError: If the response contains an HTTP error status code other than 429.
    """

    response = requests.get(url)
    while response.status_code == 429:
        logger.info(f'Rate limited. Waiting {sleep_time}s...')
        time.sleep(sleep_time)
        response = requests.get(url)
    response.raise_for_status()
    return response


def is_match(str1: str, str2: str, threshold: int = 55) -> tuple[bool, int]:
    str1 = str1.replace('_', ' ')
    str2 = str2.replace('_', ' ')
    score = fuzz.partial_ratio(str1, str2)
    return score >= threshold, score


def depluralize(word: str) -> str:
    return word[:-1] if word.endswith('s') else word
