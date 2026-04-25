import os
from re import S
import warnings
from models.layout import Layout
from models.score import Score
import time

warnings.filterwarnings("ignore")

from bs4 import BeautifulSoup
from lxml import html
from lxml.html import HtmlElement
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.round import Round
from models.event import Event
from util.consts import Consts
from util.requests import get_request_avoid_rate_limit
from datetime import datetime
from itertools import product
from logger import logger
import traceback
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def try_parse_hole_data(
    hole_elements: list[HtmlElement], num_holes: int, default: int, drop_last=True
) -> list[int]:
    if hole_elements == []:
        return [default for _ in range(num_holes)]
    try:
        if drop_last:
            return [int(x.text) for x in hole_elements[:-1]]
        else:
            return [int(x.text) for x in hole_elements]
    except:
        return [default for _ in range(num_holes)]


class Scraper:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.binary_location = os.getenv("chrome_binary_path")
        self.driver = webdriver.Chrome(
            service=Service(os.getenv("chromedriver_path")), options=options
        )

    def cleanup(self) -> None:
        self.driver.quit()

    def wait_for_xpath(self, xpath: str, timeout: int = 2) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def get_driver_page_and_wait_for_xpath(
        self, url: str, xpath: str, timeout: int = 2
    ) -> None:
        for _ in range(5):
            try:
                time.sleep(2)
                self.driver.get(url)
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                return
            except Exception as e:
                pass

        raise Exception(f"Failed to load page in 5 attempts")

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
        soup = BeautifulSoup(response.content, "html.parser")
        tree: HtmlElement = html.fromstring(str(soup))
        state_elements: list[HtmlElement] = tree.xpath(Consts.dgscene_state_xpath)
        locations = [x.text.replace(" ", "_") for x in state_elements]
        all_courses = []

        for location in locations:
            try:
                response = get_request_avoid_rate_limit(
                    f"{Consts.dgscene_courses_url}/{location}"
                )
                soup = BeautifulSoup(response.content, "html.parser")
                tree: HtmlElement = html.fromstring(str(soup))
                course_link_elements: list[HtmlElement] = tree.xpath(
                    Consts.dgscene_course_link_xpath
                )
                courses = [
                    x.get("href").replace("/courses/", "") for x in course_link_elements
                ]
                all_courses += courses
                logger.info(f"Fetch - {len(courses)} courses for {location}")
            except Exception as e:
                logger.info(f"Error - {location}: {str(e).splitlines()[0]}")

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
            response = get_request_avoid_rate_limit(
                f"{Consts.dgscene_courses_url}/{course_name}"
            )
            soup = BeautifulSoup(response.content, "html.parser")
            tree: HtmlElement = html.fromstring(str(soup))
            course_name_element: HtmlElement = tree.xpath(
                Consts.dgscene_course_name_header_xpath
            )[0]
            readable_name = course_name_element.text.strip()
            logger.info(f"Fetch - {readable_name}: {course_name}")
            return readable_name
        except Exception as e:
            logger.info(f"Error - {course_name}: {str(e).splitlines()[0]}")
            return course_name

    def get_all_sanctioned_events(
        self, course_name: str, year: int = datetime.now().year
    ) -> list[Event]:
        """
        Fetches all sanctioned event IDs for a given course name from a specified date.
        Args:
            course_name (str): The name of the course to fetch events for.
            year (int, optional): The year for which to fetch events. Defaults to the current year.
        Returns:
            list[int]: A list of sanctioned event IDs.
        Raises:
            Exception: If no PDGA results are found for an event.
            after_date (datetime, optional): The date after which events should be considered. Defaults to None.
        """
        try:
            url = Consts.dgscene_course_events_url.format(course_name=course_name)
            response = get_request_avoid_rate_limit(url)
            soup = BeautifulSoup(response.content, "html.parser")
            tree: HtmlElement = html.fromstring(str(soup))
            course_tournaments_url = tree.xpath(
                Consts.dgscene_course_tournament_link_xpath
            )[0].get("href")

            response = get_request_avoid_rate_limit(course_tournaments_url)
            soup = BeautifulSoup(response.content, "html.parser")
            tree: HtmlElement = html.fromstring(str(soup))
            sanctioned_events: list[HtmlElement] = tree.xpath(
                Consts.dgscene_sanctioned_event_xpath.format(year=year)
            )
            event_urls = [event.get("href") for event in sanctioned_events]
            logger.info(f"Fetch - {len(event_urls)} events.")
            events = []
        except Exception as e:
            logger.info(f"Error - {course_name}: {str(e).splitlines()[0]}")
            return []

        for event_url in event_urls:
            try:
                # request the dgscene event page
                response = get_request_avoid_rate_limit(event_url)
                soup = BeautifulSoup(response.content, "html.parser")
                tree: HtmlElement = html.fromstring(str(soup))
                pdga_url_elements: list[HtmlElement] = tree.xpath(
                    Consts.dgscene_pdga_event_page_xpath
                )

                if pdga_url_elements == []:
                    logger.info(f"Skip  - {event_url}: no PDGA results found")
                    continue
                else:
                    pdga_url_element = pdga_url_elements[0]
                    pdga_url: str = pdga_url_element.get("href")

                    # request the pdga event page to get date
                    response = get_request_avoid_rate_limit(pdga_url)
                    soup = BeautifulSoup(response.content, "html.parser")
                    tree: HtmlElement = html.fromstring(str(soup))
                    date_element: HtmlElement = tree.xpath(
                        Consts.pdga_event_page_date_xpath
                    )[0]
                    date_str: str = (
                        date_element.text_content().split(": ")[-1].split(" to ")[-1]
                    )
                    for month, num in Consts.month_map.items():
                        date_str = date_str.replace(month, num)
                    date = datetime.strptime(date_str, "%d-%m-%Y")

                    if date.date() > datetime.now().date():
                        logger.info(
                            f"Skip  - {pdga_url}: event date {date.date()} in the future"
                        )
                        continue

                    # get event id from pdga url
                    event_id = int(
                        pdga_url.replace(Consts.pdga_event_page_base_url, "")
                    )
                    events.append(
                        Event(event_id=event_id, course_name=course_name, date=date)
                    )

            except Exception as e:
                logger.info(f"Error - {event_url}: {str(e).splitlines()[0]}")

        return events

    def get_round_ratings_for_tournament(self, event_id: int) -> list[Round]:
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

        pdgalive_url = Consts.pdgalive_score_page_url.format(event_id=event_id)
        try:
            self.get_driver_page_and_wait_for_xpath(
                pdgalive_url, Consts.pdgalive_division_picker_xpath
            )
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            tree: HtmlElement = html.fromstring(str(soup))
            divisions: list[str] = [
                x.text for x in tree.xpath(Consts.pdgalive_division_xpath)
            ]
            rounds: list[str] = [
                x.text for x in tree.xpath(Consts.pdgalive_round_xpath)
            ]
            rating_data = []
        except Exception as e:
            logger.info(f"Error - {pdgalive_url}: {str(e).splitlines()[0]}")

        for division, round in product(divisions, rounds):
            try:
                round_number = int(round[3])
                pdga_live_url = (
                    Consts.pdgalive_score_page_specific_division_and_round_url.format(
                        event_id=event_id, division=division, round_number=round_number
                    )
                )
                self.get_driver_page_and_wait_for_xpath(
                    pdga_live_url, Consts.pdgalive_player_row_xpath
                )
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                tree: HtmlElement = html.fromstring(str(soup))

                layout_name = (
                    tree.xpath(Consts.pdgalive_layout_name_xpath)[0]
                    .text_content()
                    .strip()
                )
                num_holes = (
                    len(tree.xpath(Consts.pdgalive_layout_hole_headers_xpath)) - 1
                )
                layout_par_elements: list[HtmlElement] = tree.xpath(
                    Consts.pdgalive_layout_hole_headers_pars_xpath
                )
                layout_distance_elements: list[HtmlElement] = tree.xpath(
                    Consts.pdgalive_layout_distances_xpath
                )
                layout_hole_pars = try_parse_hole_data(
                    layout_par_elements, num_holes, 3
                )
                layout_total_par = sum(layout_hole_pars)
                layout_hole_distances = try_parse_hole_data(
                    layout_distance_elements, num_holes, 0
                )
                # print(layout_hole_distances)
                layout_total_distance = sum(layout_hole_distances)
                # print(layout_total_distance)
                # get score data
                player_rows: list[HtmlElement] = [
                    x for x in tree.xpath(Consts.pdgalive_player_row_xpath)
                ]
                num_players = len(player_rows)
                if num_players <= 1:
                    raise Exception(f"Not enough players ({num_players})")

                scores: list[Score] = []
                for row in player_rows:
                    raw_score = row.xpath(Consts.pdgalive_player_score_xpath)[
                        -1
                    ].text_content()
                    if raw_score == "DNF":
                        continue
                    elif raw_score == "E":
                        raw_score = 0
                    score = int(raw_score)
                    rating = int(
                        row.xpath(Consts.pdgalive_player_data_xpath)[-2].text_content()
                    )
                    # print(score, rating)
                    hole_scores = try_parse_hole_data(
                        row.xpath(Consts.pdgalive_hole_score_xpath),
                        num_holes,
                        -1,
                        drop_last=False,
                    )
                    score = Score(
                        rating=rating,
                        score=score,
                        hole_scores=", ".join([str(x) for x in hole_scores]),
                    )
                    scores.append(score)

                # calculate round statistics
                scores.sort(key=lambda x: x.score)
                first = scores[0]
                last = scores[-1]
                score_diff = float(last.score - first.score)
                rating_diff = float(first.rating - last.rating)
                stroke_value = rating_diff / score_diff
                par_rating = int(last.rating + (last.score * stroke_value))

                layout = Layout(
                    layout_name=layout_name,
                    num_holes=num_holes,
                    pars=", ".join([str(x) for x in layout_hole_pars]),
                    distances=", ".join([str(x) for x in layout_hole_distances]),
                    total_par=layout_total_par,
                    total_distance=layout_total_distance,
                )
                round = Round(
                    round_number=round_number,
                    num_players=num_players,
                    high_rating=first.rating,
                    low_rating=last.rating,
                    par_rating=par_rating,
                    stroke_value=stroke_value,
                    event_id=event_id,
                )

                # set relationships
                layout.round = round
                for score in scores:
                    score.round = round
                round.layout = layout
                round.scores = scores

                rating_data.append(round)

                logger.info(f"Fetch - {pdga_live_url}")
            except Exception as e:
                logger.info(f"Error - {pdga_live_url} - {str(e).splitlines()[0]}")

        return rating_data
