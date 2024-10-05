import requests
from bs4 import BeautifulSoup, Tag
import time
from logger import logger
from datetime import datetime
from lxml import html
from lxml.html import HtmlElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import regex as re

from util import get_request_avoid_rate_limit

base_url = 'https://discgolfscene.com'
course_events_url = base_url + '/courses/{course_name}/events'
pdga_event_page_base_url = 'https://www.pdga.com/tour/event/'

sanctioned_event_xpath = '''
    //a[span[
        contains(@class, 'info') and 
        contains(@class, 'ts') and (
            contains(text(), 'A-tier') or
            contains(text(), 'B-tier') or
            contains(text(), 'C-tier') or
            contains(text(), 'Major') or
            contains(text(), 'Disc Golf Pro Tour'))]]
'''
pdga_event_page_xpath = f'//a[contains(@href, "{pdga_event_page_base_url}")]'
pdga_event_page_date_xpath = '//li[contains(@class, "tournament-date")]'


month_map = {
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
}


def get_all_sanctioned_events(course_name: str, after_date: datetime = None) -> list[int]:
    """
    Fetches all sanctioned event IDs for a given course name from a specified date.
    Args:
        course_name (str): The name of the course to fetch events for.
        after_date (datetime, optional): The date after which events should be considered. Defaults to None.
    Returns:
        list[int]: A list of sanctioned event IDs.
    Raises:
        Exception: If no PDGA results are found for an event.
    """
    try:
        url = course_events_url.format(course_name=course_name)
        response = get_request_avoid_rate_limit(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tree: HtmlElement = html.fromstring(str(soup))
        sanctioned_events: list[HtmlElement] = tree.xpath(sanctioned_event_xpath)
        event_urls = [base_url + event.get('href') for event in sanctioned_events]
        event_ids = []
    except:
        return []

    for event_url in event_urls:
        try:
            logger.info(f'Fetching data for: {event_url}')

            # request the dgscene event page
            response = get_request_avoid_rate_limit(event_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            tree: HtmlElement = html.fromstring(str(soup))
            pdga_url_elements: list[HtmlElement] = tree.xpath(
                pdga_event_page_xpath)

            if pdga_url_elements == []:
                raise Exception('No PDGA results found')
            else:
                pdga_url_element = pdga_url_elements[0]
                pdga_url: str = pdga_url_element.get('href')

                # request the pdga event page to get date
                response = get_request_avoid_rate_limit(pdga_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                tree: HtmlElement = html.fromstring(str(soup))
                date_element: HtmlElement = tree.xpath(
                    pdga_event_page_date_xpath)[0]
                date_str: str = date_element.text_content().split(
                    ': ')[-1].split(' to ')[-1]
                for month, num in month_map.items():
                    date_str = date_str.replace(month, num)
                date = datetime.strptime(date_str, '%d-%m-%Y')

                # reached end of events since after_date
                if after_date is not None and date < after_date:
                    return event_ids

                # get event id from pdga url
                event_id = int(pdga_url.replace(
                    pdga_event_page_base_url, ''))
                event_ids.append(event_id)
                logger.info(f'Found event id: {event_id}')

        except Exception as e:
            logger.info(f'Error: {e}')
            logger.info(f'Skipping: {event_url}')

        logger.info('')

    return event_ids
