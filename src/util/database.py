from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.base import Base
from models.course import Course
from models.event import Event
from models.round import Round
from datetime import datetime

class Database:
    def __init__(self, connection: str) -> None:
        engine = create_engine(connection)
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        self.session: Session = session()

    def merge_rounds(self, rounds: list[Round]) -> None:
        for round in rounds:
            self.session.merge(round)

        self.session.commit()

    def merge_events(self, events: list[Event]) -> None:
        for event in events:
            self.session.merge(event)

        self.session.commit()

    def merge_data(self, course: Course, events: list[Event] = [], rounds: list[Round] = []) -> None:
        self.session.merge(course)

        for event in events:
            self.session.merge(event)

        for round in rounds:
            self.session.merge(round)

        self.session.commit()    
        
    def event_exists(self, event_id: int) -> bool:
        return self.session.query(Event).filter_by(event_id=event_id).first() is not None
        
    def event_contains_round_data(self, event_id: int) -> bool:
        return self.session.query(Round).filter_by(event_id=event_id).first() is not None
    
    def delete_event(self, event_id: int) -> None:
        self.session.query(Event).filter_by(event_id=event_id).delete()
        self.session.commit()
    
    def query_courses(self) -> list[Course]:
        all_courses = self.session.query(Course).all()
        return all_courses
    
    def query_courses_with_no_events(self) -> list[Course]:
        subquery = self.session.query(Event.course_name).distinct()
        courses_no_events = (
            self.session.query(Course)
            .filter(Course.course_name.notin_(subquery))
            .all()
        )
        return courses_no_events
    
    def query_events(self) -> list[Event]:
        all_events = self.session.query(Event).all()
        return all_events
    
    def query_events_with_no_rounds(self) -> list[Event]:
        subquery = self.session.query(Round.event_id).distinct()
        events_no_rounds = (
            self.session.query(Event)
            .filter(Event.event_id.notin_(subquery))
            .all()
        )
        return events_no_rounds
    
    def query_rounds_for_course(self, readable_course_name: str) -> list[Round]:
        course = self.session.query(Course).filter(Course.readable_course_name.ilike(readable_course_name)).first()
        
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
    
    def close(self) -> None:
        self.session.close()
