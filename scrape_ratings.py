import requests
from bs4 import BeautifulSoup, Tag
import time
from logger import logger
from datetime import datetime
from lxml import html
from lxml.html import HtmlElement
from lxml.etree import _ElementUnicodeResult
from itertools import product
import regex as r
from fuzzywuzzy import process, fuzz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import threading

# URLs
base_url = 'https://www.pdga.com/apps/tournament/live'
score_page_url = base_url + '/event?eventId={event_id}'
score_page_specific_division_and_round_url = base_url + \
    '/event?eventId={event_id}&division={division}&view=Scores&round={round_number}'


# XPaths
division_picker_xpath = '//div[contains(@class, "division-picker")]'
division_xpath = division_picker_xpath + '//button[not(text()="Leaders")]'
round_picker_xpath = division_picker_xpath + '/following-sibling::div[1]'
round_xpath = round_picker_xpath + '//div[contains(text(), "Rd")]'
round_course_metadata_xpath = '//div[contains(@class, "round-course-meta")]'
round_course_metadata_text_xpath = round_course_metadata_xpath + '//text()'
course_layout_xpath = '//div[contains(@class, "course-meta")]//i[contains(@class, "pi-course-layout")]/parent::*'
course_name_xpath = '//div[contains(@class, "course-meta")]//i[contains(@class, "pi-course-icon")]/parent::*'
layout_par_xpath = "//div[contains(@class, 'header-col') and contains(string(),'Tot')]//div[contains(@class, 'label-2')]"
player_row_xpath = '//div[contains(@class, "table-row-content")]'
player_score_xpath = "//div[contains(@class, 'round-score')]"
player_rating_xpath = "//div[contains(@class, 'cell-wrapper')]//div"
player_row_cell_xpath = "//div[contains(@class, 'cell-wrapper')]//div"


# Regexes
round_regex = r'Round (\d)'


def get_round_ratings_for_tournament(event_id: int) -> list[dict[str, list]]:
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
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        service = Service(
            executable_path='/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(score_page_url.format(event_id=event_id))
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, division_picker_xpath)))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tree: HtmlElement = html.fromstring(str(soup))
        divisions: list[str] = [x.text for x in tree.xpath(division_xpath)]
        rounds: list[str] = [x.text for x in tree.xpath(round_xpath)]
        rating_data = []
    except Exception as e:
        logger.info(e)
        return []

    for division, round in product(divisions, rounds):
        try:
            round_number = int(round[3])
            driver.get(score_page_specific_division_and_round_url.format(
                event_id=event_id, division=division, round_number=round_number))
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, player_row_xpath)))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            tree: HtmlElement = html.fromstring(str(soup))
            course_name = tree.xpath(course_name_xpath)[
                0].text_content().strip()
            course_layout = tree.xpath(course_layout_xpath)[
                0].text_content().strip()

            # get low, high rating and calculate average
            layout_par = int(tree.xpath(layout_par_xpath)[0].text)
            player_rows: list[HtmlElement] = [x for x in tree.xpath(
                player_row_xpath) if 'DNF' not in x.text_content()]

            # first player data
            first_player_row: HtmlElement = player_rows[0]
            first_player_raw_score = int(
                first_player_row.xpath('.' + player_row_cell_xpath)[-2].text)
            first_player_score = first_player_raw_score - layout_par
            first_player_rating = int(
                first_player_row.xpath('.' + player_row_cell_xpath)[-1].text)
            # last player data
            last_player_row: HtmlElement = player_rows[-1]
            last_player_raw_score = int(
                last_player_row.xpath('.' + player_row_cell_xpath)[-2].text)
            last_player_score = last_player_raw_score - layout_par
            last_player_rating = int(last_player_row.xpath(
                '.' + player_row_cell_xpath)[-1].text)

            # calculate round statistics
            score_diff = float(last_player_score - first_player_score)
            rating_diff = float(first_player_rating - last_player_rating)
            stroke_value = rating_diff / score_diff
            par_rating = int(last_player_rating +
                             (last_player_score * stroke_value))
            round_data = {
                'course_name': course_name,
                'course_layout': course_layout,
                'round': round_number,
                'players': len(player_rows),
                'par': layout_par,
                'high_rating': first_player_rating,
                'low_rating': last_player_rating,
                'stroke_value': stroke_value,
                'par_rating': par_rating
            }
            rating_data.append(round_data)
        except Exception as e:
            pass

    driver.quit()
    return rating_data
