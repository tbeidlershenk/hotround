from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Course(Base):
    __tablename__ = 'Courses'
    course_name = Column(String(100), unique=True, primary_key=True, nullable=False)
    readable_course_name = Column(String(100), nullable=False)
