from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.base import Base
import json

class Course(Base):
    __tablename__ = "Courses"
    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(100), nullable=False)
    course_text = Column(String(200), nullable=True)
    events = relationship("Event", back_populates="course")

    def to_dict(self) -> dict:
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "course_text": self.course_text
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())
    
    def from_json(json_str: str):
        dict = json.loads(json_str)
        course = Course()
        course.course_id = dict["course_id"]
        course.course_name = dict["course_name"]
        course.course_text = dict["course_text"]
        return course
    
    def get_name(self) -> str:
        if self.course_text is None:
            return self.course_name.replace('_', ' ')
        elif '\n\n' not in self.course_text:
            return self.course_name.replace('_', ' ')
        else:
            return self.course_text.split('\n\n')[0]
        
    def get_name_tokens(self) -> str:
        name = self.get_name()
        name_lower = name.lower()
        return name_lower.split(' ')
        
    def get_location(self) -> str:
        if self.course_text is None:
            return ''
        elif '\n\n' not in self.course_text:
            return ''
        else:
            return self.course_text.split('\n\n')[1]
        
    

# from sqlalchemy import Column, String, Integer
# from sqlalchemy.orm import relationship
# from models.base import Base


# class Course(Base):
#     __tablename__ = "Courses"
#     course_name = Column(String(100), nullable=False)
#     readable_course_name = Column(String(100), nullable=False)
#     course_text = Column(String(200), nullable=True)
#     course_id = Column(Integer, primary_key=True)
#     events = relationship("Event", back_populates="course")

#     def to_dict(self) -> dict:
#         return {
#             "course_name": self.course_name,
#             "readable_course_name": self.readable_course_name,
#             "course_text": self.course_location,
#             "course_id": self.course_location,
#         }
