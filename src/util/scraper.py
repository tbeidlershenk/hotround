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
from models.course import Course
from util.consts import Consts
from util.requests import get_request_avoid_rate_limit
from datetime import datetime
from itertools import product
from logger import logger
import traceback
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from util.helpers import to_pdgalive_link, try_parse_hole_data

class Scraper:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # IMPORTANT (old headless is deprecated)
        options.add_argument("--no-sandbox")  # REQUIRED on many servers
        options.add_argument("--disable-dev-shm-usage")  # prevents crashes in /dev/shm
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.binary_location = os.getenv("chrome_binary_path")
        self.driver = webdriver.Chrome(options=options)

    def cleanup(self) -> None:
        self.driver.quit()

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
    
    def get_locations_dgscene(self) -> list[str]:
        response = get_request_avoid_rate_limit(Consts.dgscene_courses_url, sleep_time=5)
        soup = BeautifulSoup(response.content, "html.parser")
        tree: HtmlElement = html.fromstring(str(soup))
        state_elements: list[HtmlElement] = tree.xpath('//div[contains(@class, "list-record")]//a[contains(@href, "/courses/")]')
        locations = [x.get("href").replace("/courses/", "") for x in state_elements]
        return locations

    def get_courses_dgscene(self, location: str) -> list[Course]:
        location_courses = []
        response = get_request_avoid_rate_limit(f"https://discgolfscene.com/courses/{location}", sleep_time=5)
        soup = BeautifulSoup(response.content, "html.parser")
        tree: HtmlElement = html.fromstring(str(soup))
        course_link_elements: list[HtmlElement] = tree.xpath('//a[contains(@href, "discgolfscene.com/course")]')
        for course_element in course_link_elements:
            try:
                course_href = course_element.get("href")
                course = Course()
                course.course_id = course_href.split("course/")[1].split("/")[0]
                course.course_name = course_href.split("/")[-1]
                course.course_text = course_element.text_content()
                #course.course_text = course.course_text.replace("\n", "")
                course.course_text = course.course_text.replace("\t", "")
                course.course_text = course.course_text.strip()
                location_courses.append(course)
            except Exception as e:
                logger.info(f"Error scraping location {location}: {str(e).splitlines()[0]}")

        return location_courses

    def get_events_dgscene(self, course_id: int, year: int = datetime.now().year) -> list[Event]:

        # define xpaths and urls
        dgscene_course_tournament_link_xpath = '//a[contains(@href, "/tournaments") and contains(@href, "/course")]'
        dgscene_sanctioned_event_xpath = '//div[contains(@class, "tournament-list list-record")]//a[contains(string(), "{year}")]'
        dgscene_pdga_event_page_xpath = "//div[contains(@class, 'pdga-results-link')]//a"
        pdga_event_page_date_xpath = '//li[contains(@class, "tournament-date")]'
        pdga_event_page_base_url = "https://www.pdga.com/tour/event/"
        dgscene_course_events_url = "https://discgolfscene.com/course/{course_id}"

        try:
            url = dgscene_course_events_url.format(course_id=course_id)
            response = get_request_avoid_rate_limit(url)
            soup = BeautifulSoup(response.content, "html.parser")
            tree: HtmlElement = html.fromstring(str(soup))
            course_tournaments_url = tree.xpath(dgscene_course_tournament_link_xpath)[0].get("href")

            response = get_request_avoid_rate_limit(course_tournaments_url)
            soup = BeautifulSoup(response.content, "html.parser")
            tree: HtmlElement = html.fromstring(str(soup))
            sanctioned_events: list[HtmlElement] = tree.xpath(dgscene_sanctioned_event_xpath.format(year=year))
            
            event_urls = [event.get("href") for event in sanctioned_events]
            events = []
        except Exception as e:
            logger.info(f"Error scraping course {course_id}: {str(e).splitlines()[0]}")
            return []

        for event_url in event_urls:
            try:
                # request the dgscene event page
                response = get_request_avoid_rate_limit(event_url)
                soup = BeautifulSoup(response.content, "html.parser")
                tree: HtmlElement = html.fromstring(str(soup))
                pdga_url_elements: list[HtmlElement] = tree.xpath(dgscene_pdga_event_page_xpath)

                if pdga_url_elements == []:
                    raise Exception(f"No PDGA results found")
                else:
                    pdga_url_element = pdga_url_elements[0]
                    pdga_url: str = pdga_url_element.get("href")

                    # request the pdga event page to get date
                    response = get_request_avoid_rate_limit(pdga_url)
                    soup = BeautifulSoup(response.content, "html.parser")
                    tree: HtmlElement = html.fromstring(str(soup))
                    date_element: HtmlElement = tree.xpath(pdga_event_page_date_xpath)[0]
                    date_str: str = date_element.text_content().split(": ")[-1].split(" to ")[-1]

                    for month, num in Consts.month_map.items():
                        date_str = date_str.replace(month, num)
                    date = datetime.strptime(date_str, "%d-%m-%Y")

                    if date.date() > datetime.now().date():
                        raise Exception(f"Event date in the future ({date.date()})")

                    # get event id from pdga url
                    event_id = int(pdga_url.replace(pdga_event_page_base_url, ""))
                    event = Event(event_id=event_id, course_id=course_id, date=date)
                    events.append(event)

            except Exception as e:
                logger.info(f"Error scraping event {event_url.split('/')[-1]}: {str(e).splitlines()[0]}")

        return events

    def get_ratings_pdgalive(self, event_id: int) -> list[Round]:

        pdgalive_base_url = "https://www.pdga.com/apps/tournament/live"
        pdgalive_score_page_url = pdgalive_base_url + "/event?eventId={event_id}"
        pdgalive_score_page_specific_division_and_round_url = pdgalive_base_url + "/event?eventId={event_id}&division={division}&view=Scores&round={round_number}"
        pdgalive_division_picker_xpath = '//div[contains(@class, "division-picker")]'
        pdgalive_division_xpath = '//div[contains(@class, "division-picker")]//button[not(text()="Leaders")]'
        pdgalive_round_xpath = '//a[contains(string(), "Rd")]'
        pdgalive_player_row_xpath = '//div[contains(@class, "table-row-content")]'
        pdgalive_layout_name_xpath = '//div[i[contains(@class, "pi-course-layout")]]'
        pdgalive_layout_hole_headers_xpath = "//div[contains(@class, 'header-row')]//div[contains(@id, 'hole')]"
        pdgalive_layout_hole_headers_pars_xpath = "//div[contains(@class, 'header-row')]//div[contains(@id, 'hole')]//div[contains(@class, 'label-2')][2]"
        pdgalive_layout_distances_xpath = "//div[contains(@class, 'header-row')]//div[contains(@id, 'hole')]//span"
        pdgalive_player_score_xpath = ".//div[contains(@class, 'round-score')]"
        pdgalive_player_data_xpath = ".//div[contains(@class, 'cell-wrapper')]"
        pdgalive_hole_score_xpath = ".//div[contains(@class, 'hs')]"

        pdgalive_url = pdgalive_score_page_url.format(event_id=event_id)

        divisions = []
        rounds = []
        rating_data = []

        try:
            self.get_driver_page_and_wait_for_xpath(pdgalive_url, pdgalive_division_picker_xpath, timeout=5)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            tree: HtmlElement = html.fromstring(str(soup))
            divisions: list[str] = [x.text for x in tree.xpath(pdgalive_division_xpath)]
            rounds: list[str] = [x.text for x in tree.xpath(pdgalive_round_xpath)]
        except Exception as e:
            logger.info(f"Error scraping event {event_id} - {str(e).splitlines()[0]}")

        for division, round in product(divisions, rounds):
            try:
                round_number = -1
                if len(round) <= 4:
                    round_number = int(round[3])
                pdgalive_url = pdgalive_score_page_specific_division_and_round_url.format(event_id=event_id, division=division, round_number=round_number)
                self.get_driver_page_and_wait_for_xpath(pdgalive_url, pdgalive_player_row_xpath, timeout=5)
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                tree: HtmlElement = html.fromstring(str(soup))

                layout_name = tree.xpath(pdgalive_layout_name_xpath)[0].text_content().strip()
                num_holes = len(tree.xpath(pdgalive_layout_hole_headers_xpath)) - 1
                layout_par_elements: list[HtmlElement] = tree.xpath(pdgalive_layout_hole_headers_pars_xpath)
                layout_distance_elements: list[HtmlElement] = tree.xpath(pdgalive_layout_distances_xpath)
                layout_hole_pars = try_parse_hole_data(layout_par_elements, num_holes, 3)
                layout_total_par = sum(layout_hole_pars)
                layout_hole_distances = try_parse_hole_data(layout_distance_elements, num_holes, 0)
                layout_total_distance = sum(layout_hole_distances)
                # get score data
                player_rows: list[HtmlElement] = [
                    x for x in tree.xpath(pdgalive_player_row_xpath)
                ]
                num_players = len(player_rows)
                if num_players <= 1:
                    raise Exception(f"Not enough players ({num_players})")

                scores: list[Score] = []
                for row in player_rows:
                    raw_score = row.xpath(pdgalive_player_score_xpath)[
                        -1
                    ].text_content()
                    if raw_score == "DNF":
                        continue
                    elif raw_score == "E":
                        raw_score = 0
                    score = int(raw_score)
                    rating = int(
                        row.xpath(pdgalive_player_data_xpath)[-2].text_content()
                    )
                    # print(score, rating)
                    hole_scores = try_parse_hole_data(row.xpath(pdgalive_hole_score_xpath), num_holes, -1, drop_last=False)
                    hole_scores_str = ", ".join([str(x) for x in hole_scores])
                    score = Score(rating=rating, score=score, hole_scores=hole_scores_str)
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

            except Exception as e:
                logger.info(f"Error scraping round {event_id}, {division}, {round} - {str(e).splitlines()[0]}")

        return rating_data
