from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Event(Base):
    __tablename__ = 'Events'
    event_id = Column(Integer, primary_key=True, nullable=False)
    date = Column(Date, nullable=False)
    course_name = Column(String(100), ForeignKey('Courses.course_name', ondelete='CASCADE'), nullable=False)
