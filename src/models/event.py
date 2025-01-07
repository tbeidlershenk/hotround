from sqlalchemy import Column, Integer, String, Date, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship

class Event(Base):
    __tablename__ = 'Events'
    event_id = Column(Integer, primary_key=True, nullable=False)
    date = Column(Date, nullable=False)
    course_name = Column(String(100), ForeignKey('Courses.course_name', ondelete='CASCADE'), nullable=False, index=True)
    course = relationship('Course', back_populates='events')
    rounds = relationship('Round', back_populates='event')

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "date": self.date,
            "course_name": self.course_name,
            "course": self.course.to_dict(),
        }