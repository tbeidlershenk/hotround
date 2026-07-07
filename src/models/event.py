from sqlalchemy import Column, Integer, String, Date, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship

from datetime import datetime
import json

class Event(Base):
    __tablename__ = 'Events'
    event_id = Column(Integer, primary_key=True, nullable=False)
    course_id = Column(Integer, ForeignKey('Courses.course_id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False)
    course = relationship('Course', back_populates='events')
    rounds = relationship('Round', back_populates='event')

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "course_id": self.course_id,
            "date": self.date,
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())
    
    def from_json(json_str: str):
        dict = json.loads(json_str)
        event = Event()
        event.event_id = dict["event_id"]
        event.course_id = dict["course_id"]
        event.date = datetime.fromisoformat(dict["date"])
        return event