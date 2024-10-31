from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.base import Base
from models.course import Course
from models.event import Event
from models.round import Round
from datetime import datetime
from logger import logger
from sqlalchemy.orm import joinedload

class Database:
    def __init__(self, connection: str) -> None:
        engine = create_engine(connection)
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        self.session: Session = session()

    def insert_course_data(self, data: dict) -> None:
        course = Course(
            course_name=data['course_name'],
            readable_course_name=data['readable_course_name']
        )
        events = [
            Event(
                event_id=event['event_id'],
                date=datetime.strptime(event['date'], '%d-%m-%Y'),
                course_name=data['course_name'],
            )
            for event in data['events']
        ]
        rounds = [
            Round(
                layout_name=round['layout_name'],
                round_number=round['round_number'],
                num_players=round['num_players'],
                layout_par=round['layout_par'],
                layout_distance=round['layout_distance'],
                high_rating=round['high_rating'],
                low_rating=round['low_rating'],
                par_rating=round['par_rating'],
                stroke_value=round['stroke_value'],
                event_id=round['event_id'],
            )
            for round in data['rounds']
        ]
        self.session.merge(course)
        for event in events:
            self.session.merge(event)
        for round in rounds:
            self.session.merge(round)

        self.session.commit()
        logger.info(f'Inserted course data for {data["course_name"]}')
        return True
        
    def event_exists(self, event_id: int) -> bool:
        return self.session.query(Event).filter_by(event_id=event_id).first() is not None
        
    def query_all_courses(self) -> list[Course]:
        all_courses = self.session.query(Course).all()
        return all_courses
    
    def query_all_course_rounds(self, readable_course_name: str) -> list[Round]:
        course = self.session.query(Course).filter_by(readable_course_name=readable_course_name).first()
        if not course:
            return []
        
        course_name = course.course_name
        all_rounds = (
            self.session.query(Round)
            .join(Event, Round.event_id == Event.event_id)
            .filter(Event.course_name == course_name)
            .all()
        )
        return all_rounds
