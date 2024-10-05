import requests
from bs4 import BeautifulSoup, Tag
import time
from logger import logger
from util import get_request_avoid_rate_limit
from lxml import html
from lxml.html import HtmlElement

base_url = 'https://discgolfscene.com/courses'
state_xpath = '''
    //div[contains(@class, "statelist")]
    //div
    //*
'''
course_link_xpath = '''
    //div[contains(@id, "courses-big-listing")]
    //a[contains(@href, "/courses/") and @title]
'''
course_name_header_xpath = '//h1[contains(@class, "header-location")]'


def get_courses_from_dgscene() -> list[str]:
    """
    Fetches a list of courses from the DGScene website.
    This function sends HTTP requests to the base URL and its subpages to scrape
    course information. It parses the HTML content to extract course links and
    compiles a list of course identifiers.
    Returns:
        list[str]: A list of course identifiers extracted from the website.
    """

    response = get_request_avoid_rate_limit(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tree: HtmlElement = html.fromstring(str(soup))
    state_elements: list[HtmlElement] = tree.xpath(state_xpath)
    locations = [x.text.replace(' ', '_') for x in state_elements]
    all_courses = []

    for location in locations:
        try:
            response = get_request_avoid_rate_limit(f'{base_url}/{location}')
            soup = BeautifulSoup(response.content, 'html.parser')
            tree: HtmlElement = html.fromstring(str(soup))
            course_link_elements: list[HtmlElement] = tree.xpath(
                course_link_xpath)
            courses = [x.get('href').replace('/courses/', '')
                       for x in course_link_elements]
            all_courses += courses
            logger.info(f'Fetched {len(courses)} courses for {location}')
        except Exception as e:
            logger.info(f'Error fetching courses for {location}: {e}')

    return all_courses


def get_readable_course_name(course_name: str) -> str:
    """
    Fetches and returns a human-readable course name from a given course identifier.
    Args:
        course_name (str): The identifier of the course to fetch the readable name for.
    Returns:
        str: The human-readable course name.
    """
    try:
        response = get_request_avoid_rate_limit(f'{base_url}/{course_name}')
        soup = BeautifulSoup(response.content, 'html.parser')
        tree: HtmlElement = html.fromstring(str(soup))
        course_name_element: HtmlElement = tree.xpath(
            course_name_header_xpath)[0]
        readable_name = course_name_element.text.strip()
        logger.info(f'Fetched {readable_name} for {course_name}')
        return readable_name
    except Exception as e:
        logger.info(f'Error fetching readable name for {course_name}: {e}')
        return course_name
