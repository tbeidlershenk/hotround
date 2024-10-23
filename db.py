import json
from sqlite3 import Cursor
from logger import logger
from mysql import connector
from dotenv import load_dotenv
import os

INSERT_COURSES = """
    INSERT INTO Courses 
    (
        course_name, 
        readable_course_name
    )
    VALUES 
    (
        '%s', 
        '%s'
    );
"""

INSERT_EVENTS = """
    INSERT INTO Events 
    (
        event_id, 
        course_id, 
        date
    )
    VALUES 
    (
        %s, 
        (SELECT course_id FROM Courses c WHERE c.course_name = '%s'), 
        STR_TO_DATE(%s, '%d-%m-%Y')
    );
"""

INSERT_ROUNDS = """
    INSERT INTO Rounds 
    (
        layout_name, 
        round_number, 
        num_players, 
        layout_par, 
        high_rating, 
        low_rating, 
        par_rating, 
        stroke_value, 
        event_id
    )
    VALUES 
    (
        '%s', 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s
    );
"""

def insert_course(connection, data: dict) -> bool:
    try:
        cursor = connection.cursor()
        cursor.execute(INSERT_COURSES % (data['course_name'], data['readable_course_name']))
        connection.commit()

        events_list = [(event['event_id'], data['course_name'], event['date']) for event in data['events']]
        cursor.executemany(INSERT_EVENTS, events_list)
        connection.commit()

        rounds_list = [(
            round_data['layout_name'],
            round_data['round_number'],
            round_data['num_players'],
            round_data['layout_par'],
            round_data['high_rating'],
            round_data['low_rating'],
            round_data['par_rating'],
            round_data['stroke_value'],
            round_data['event_id'])
            for round_data in data['rounds']
        ]
        cursor.executemany(INSERT_ROUNDS, rounds_list)
        connection.commit()
        return True
    except Exception as e:
        
        logger.error(f"Error inserting course data: {e}")
        connection.rollback()
        return False

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

connection = connector.connect(
    host="localhost",
    user="pdga_rating_bot",
    password="BluePancakes1*",
    database="pdgaratingsdb"
)

with open('test/test_course_data.json', 'r') as file:
    course_data: dict = json.load(file)

result = insert_course(connection, course_data)

