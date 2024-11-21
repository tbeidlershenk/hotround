from sqlalchemy import Column, Integer, String, Date, ForeignKey
from models.base import Base

class Event(Base):
    __tablename__ = 'Events'
    event_id = Column(Integer, primary_key=True, nullable=False)
    date = Column(Date, nullable=False)
    course_name = Column(String(100), ForeignKey('Courses.course_name', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "date": self.date,
            "course_name": self.course_name
        }