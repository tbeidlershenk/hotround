import requests
from bs4 import BeautifulSoup, Tag
import time
from logger import logger
from util.requests import get_request_avoid_rate_limit
from lxml import html
from lxml.html import HtmlElement
from typing import Any
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
from util.consts import Consts
from bs4 import BeautifulSoup
from logger import logger
from lxml import html
from lxml.html import HtmlElement
from itertools import product
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util.requests import get_request_avoid_rate_limit

class Scraper:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)


    def cleanup(self) -> None:
        self.driver.quit()


    def get_courses_from_dgscene(self) -> list[str]:
        """
        Fetches a list of courses from the DGScene website.
        This function sends HTTP requests to the base URL and its subpages to scrape
        course information. It parses the HTML content to extract course links and
        compiles a list of course identifiers.
        Returns:
            list[str]: A list of course identifiers extracted from the website.
        """

        response = get_request_avoid_rate_limit(Consts.dgscene_courses_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tree: HtmlElement = html.fromstring(str(soup))
        state_elements: list[HtmlElement] = tree.xpath(Consts.dgscene_state_xpath)
        locations = [x.text.replace(' ', '_') for x in state_elements]
        all_courses = []

        for location in locations:
            try:
                response = get_request_avoid_rate_limit(f'{Consts.dgscene_courses_url}/{location}')
                soup = BeautifulSoup(response.content, 'html.parser')
                tree: HtmlElement = html.fromstring(str(soup))
                course_link_elements: list[HtmlElement] = tree.xpath(
                    Consts.dgscene_course_link_xpath)
                courses = [x.get('href').replace('/courses/', '')
                        for x in course_link_elements]
                all_courses += courses
                logger.info(f'Fetched {len(courses)} courses for {location}')
            except Exception as e:
                logger.info(f'Error fetching courses for {location}: {e}')

        return all_courses


    def get_readable_course_name(self, course_name: str) -> str:
        """
        Fetches and returns a human-readable course name from a given course identifier.
        Args:
            course_name (str): The identifier of the course to fetch the readable name for.
        Returns:
            str: The human-readable course name.
        """
        try:
            response = get_request_avoid_rate_limit(f'{Consts.dgscene_courses_url}/{course_name}')
            soup = BeautifulSoup(response.content, 'html.parser')
            tree: HtmlElement = html.fromstring(str(soup))
            course_name_element: HtmlElement = tree.xpath(
                Consts.dgscene_course_name_header_xpath)[0]
            readable_name = course_name_element.text.strip()
            logger.info(f'Fetched {readable_name} for {course_name}')
            return readable_name
        except Exception as e:
            logger.info(f'Error fetching readable name for {course_name}: {e}')
            return course_name


    def get_all_sanctioned_events(self, course_name: str, after_date: datetime = None) -> dict:
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
            url = Consts.dgscene_course_events_url.format(course_name=course_name)
            response = get_request_avoid_rate_limit(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            tree: HtmlElement = html.fromstring(str(soup))
            sanctioned_events: list[HtmlElement] = tree.xpath(
                Consts.dgscene_sanctioned_event_xpath)
            event_urls = [Consts.dgscene_base_url + event.get('href')
                        for event in sanctioned_events]
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
                    Consts.dgscene_pdga_event_page_xpath)

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
                        Consts.dgscene_pdga_event_page_date_xpath)[0]
                    date_str: str = date_element.text_content().split(
                        ': ')[-1].split(' to ')[-1]
                    for month, num in Consts.month_map.items():
                        date_str = date_str.replace(month, num)
                    date = datetime.strptime(date_str, '%d-%m-%Y')

                    # reached end of events since after_date
                    if after_date is not None and date < after_date:
                        return event_ids

                    # get event id from pdga url
                    event_id = int(pdga_url.replace(
                        Consts.pdga_event_page_base_url, ''))
                    event_ids.append({
                        'event_id': event_id,
                        'date': date_str
                    })
                    logger.info(f'Found event id: {event_id}')

            except Exception as e:
                logger.info(f'Error: {e}')
                logger.info(f'Skipping: {event_url}')

            logger.info('')

        return event_ids


    def get_round_ratings_for_tournament(self, event_id: int) -> list[dict[str, list]]:
        """
        Fetches and calculates round ratings for a given tournament event.
        Args:
            event_id (int): The unique identifier for the tournament event.
        Returns:
            dict[str, list]: A dictionary where keys are layout data strings and values are dictionaries containing:
                - 'round' (int): The round number.
                - 'players' (int): The number of players in the round.
                - 'high_rating' (int): The highest player rating in the round.
                - 'low_rating' (int): The lowest player rating in the round.
                - 'stroke_value' (float): The value of each stroke in terms of rating points.
                - 'par_rating' (int): The calculated rating for par.
        Raises:
            Exception: If there is an error fetching or processing the rating data for any division or round.
        """

        try:
            self.driver.get(Consts.pdgalive_score_page_url.format(event_id=event_id))
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, Consts.pdgalive_division_picker_xpath)))

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            tree: HtmlElement = html.fromstring(str(soup))
            divisions: list[str] = [x.text for x in tree.xpath(Consts.pdgalive_division_xpath)]
            rounds: list[str] = [x.text for x in tree.xpath(Consts.pdgalive_round_xpath)]
            rating_data = []
        except Exception as e:
            logger.info(e)
            return []

        for division, round in product(divisions, rounds):
            try:
                round_number = int(round[3])
                self.driver.get(Consts.pdgalive_score_page_specific_division_and_round_url.format(
                    event_id=event_id, division=division, round_number=round_number))
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, Consts.pdgalive_player_row_xpath)))
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                tree: HtmlElement = html.fromstring(str(soup))
                course_name = tree.xpath(Consts.pdgalive_course_name_xpath)[
                    0].text_content().strip()
                course_layout = tree.xpath(Consts.pdgalive_course_layout_xpath)[
                    0].text_content().strip()

                # get low, high rating and calculate average
                layout_par = int(tree.xpath(Consts.pdgalive_layout_par_xpath)[0].text)
                layout_distance = int(tree.xpath(Consts.pdgalive_layout_distance_xpath)[0].text.replace('\'', ''))
                player_rows: list[HtmlElement] = [x for x in tree.xpath(
                    Consts.pdgalive_player_row_xpath) if 'DNF' not in x.text_content()]

                # first player data
                first_player_row: HtmlElement = player_rows[0]
                first_player_raw_score = int(
                    first_player_row.xpath('.' + Consts.pdgalive_player_row_cell_xpath)[-2].text)
                first_player_score = first_player_raw_score - layout_par
                first_player_rating = int(
                    first_player_row.xpath('.' + Consts.pdgalive_player_row_cell_xpath)[-1].text)
                # last player data
                last_player_row: HtmlElement = player_rows[-1]
                last_player_raw_score = int(
                    last_player_row.xpath('.' + Consts.pdgalive_player_row_cell_xpath)[-2].text)
                last_player_score = last_player_raw_score - layout_par
                last_player_rating = int(last_player_row.xpath(
                    '.' + Consts.pdgalive_player_row_cell_xpath)[-1].text)

                # calculate round statistics
                score_diff = float(last_player_score - first_player_score)
                rating_diff = float(first_player_rating - last_player_rating)
                stroke_value = rating_diff / score_diff
                par_rating = int(last_player_rating +
                                (last_player_score * stroke_value))
                round_data = {
                    'event_id': event_id,
                    'course_name': course_name,
                    'layout_name': course_layout,
                    'round_number': round_number,
                    'num_players': len(player_rows),
                    'layout_par': layout_par,
                    'layout_distance': layout_distance,
                    'high_rating': first_player_rating,
                    'low_rating': last_player_rating,
                    'stroke_value': stroke_value,
                    'par_rating': par_rating
                }
                rating_data.append(round_data)
            except Exception as e:
                pass

        return rating_data
