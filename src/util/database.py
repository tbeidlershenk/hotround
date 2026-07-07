from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, joinedload
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

    def merge_data(self, course: Course, events: list[Event] = [], rounds: list[Round] = []) -> None:
        self.session.merge(course)
        for event in events:
            self.session.merge(event)
        for round in rounds:
            self.session.merge(round)
        self.session.commit()

    def event_exists(self, event_id: int) -> bool:
        return (
            self.session.query(Event)
            .filter_by(event_id=event_id)
            .first() is not None
        )

    def event_contains_round_data(self, event_id: int) -> bool:
        return (
            self.session.query(Round)
            .filter_by(event_id=event_id)
            .first() is not None
        )
    
    def query_course(self, course_id: int) -> Course:
        return (
            self.session.query(Course)            
            .filter(Course.course_id == course_id)
            .first()
        )

    def query_courses(self) -> list[Course]:
        return self.session.query(Course).all()
    
    def query_course_with_name(self, course_name: str) -> Course:
        return (
            self.session.query()
            .filter(Course.course_name == course_name)
            .first()
        )

    def query_courses_with_no_events(self) -> list[Course]:
        subquery = self.session.query(Event.course_name).distinct()
        return (
            self.session.query(Course)
            .filter(Course.course_name.notin_(subquery))
            .all()
        )

    def query_events(self) -> list[Event]:
        return self.session.query(Event).all()
    
    def query_events_for_course(self, course_id: int) -> list[Event]:
        return (
            self.session.query(Event)
            .filter(Event.course_id == course_id)
            .all()
        )

    def query_most_recent_event_date(self, course_id: str) -> datetime:
        most_recent_event = (
            self.session.query(Event)
            .filter(Event.course_id == course_id)
            .order_by(Event.date.desc())
            .first()
        )
        return most_recent_event.date if most_recent_event else datetime.min

    def query_events_with_no_rounds(self) -> list[Event]:
        subquery = (
            self.session.query(Round.event_id)
            .distinct()
        )
        return (
            self.session.query(Event)
            .filter(Event.event_id.notin_(subquery))
            .all()
        )

    def query_rounds_for_course(self, course_id: int) -> list[Round]:
        return (
            self.session.query(Round)
            .filter(Event.course_id == course_id)
            .join(Event, Round.event_id == Event.event_id)
            .all()
        )

    def query_aggregate_layouts(self, course_id: int) -> list[AggregateLayout]:
        layouts_rounds = (
            self.session.query(Round)
            .filter(Event.course_id == course_id)
            .join(Event, Round.event_id == Event.event_id)
            .options(joinedload(Round.scores), joinedload(Round.layout))
            .all()
        )
        data = aggregate_layouts(layouts_rounds)
        return data

    def close(self) -> None:
        self.session.close()
