import logging
import time
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none"
}


def get_request_avoid_rate_limit(url: str, sleep_time: int = 2) -> requests.Response:
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
    time.sleep(sleep_time)
    return response
