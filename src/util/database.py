from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.base import Base
from models.course import Course
from models.event import Event
from models.layout import AggregateLayout, Layout, aggregate_layouts
from models.round import Round
from datetime import datetime

from models.score import Score

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
        data = self.session.query(Course).all()
        return data
    
    def query_courses_with_no_events(self) -> list[Course]:
        subquery = self.session.query(Event.course_name).distinct()
        data = (
            self.session.query(Course)
            .filter(Course.course_name.notin_(subquery))
            .all()
        )
        return data
    
    def query_events(self) -> list[Event]:
        data = self.session.query(Event).all()
        return data
    
    def query_events_with_no_rounds(self) -> list[Event]:
        subquery = self.session.query(Round.event_id).distinct()
        data = (
            self.session.query(Event)
            .filter(Event.event_id.notin_(subquery))
            .all()
        )
        return data
    
    def query_rounds_for_course(self, readable_course_name: str) -> list[Round]:
        course = self.session.query(Course).filter(Course.readable_course_name.ilike(readable_course_name)).first()
        
        if not course:
            return []
        
        course_name = course.course_name
        data = (
            self.session.query(Round)
            .join(Event, Round.event_id == Event.event_id)
            .filter(Event.course_name == course_name)
            .all()
        )
        return data
    
    def query_aggregate_layouts(self, readable_course_name: str) -> list[AggregateLayout]:
        course = self.session.query(Course).filter(Course.readable_course_name.ilike(readable_course_name)).first()
        
        if not course:
            return []
        
        course_name = course.course_name
        layouts_rounds = (
            self.session.query(Round, Layout, Score)
            .filter(Round.round_id == Layout.round_id)
            .filter(Layout.round_id == Score.round_id)
            .join(Event, Round.event_id == Event.event_id)
            .filter(Event.course_name == course_name)
            .all()
        )
        data = aggregate_layouts(layouts_rounds)
        return data
    
    def query_scores_for_aggregate_layout(self, aggregate_layout: AggregateLayout) -> list[Score]:
        layouts = aggregate_layout.layouts
        round_ids = [x.round_id for x in layouts]
        data = (
            self.session.query(Score)
            .join(Layout, Layout.round_id == Score.round_id)
            .filter(Layout.round_id in round_ids)
            .all()
        )
        return data
    
    def close(self) -> None:
        self.session.close()