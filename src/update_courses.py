import warnings

warnings.filterwarnings("ignore")

from util.configuration import load_config_into_env
from util.database import Database
from util.scraper import Scraper
from logger import logger
from datetime import datetime, timedelta
import json
import time
import sys
import os

if len(sys.argv) == 2:
    config_file_path = sys.argv[1]
    load_config_into_env(config_file_path)

connection = os.getenv("db_connection")
database = Database(connection=connection)
scraper = Scraper()

# all_courses = scraper.get_courses_from_dgscene()
# db_courses = database.query_courses()
