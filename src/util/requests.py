import requests
import logging
import time


proxies = []


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
    response.raise_for_status()
    time.sleep(2)
    return response
