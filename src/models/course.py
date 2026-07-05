from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.base import Base


class Course(Base):
    __tablename__ = "Courses"
    course_name = Column(String(100), nullable=False)
    course_text = Column(String(200), nullable=True)
    course_id = Column(Integer, primary_key=True)
    events = relationship("Event", back_populates="course")

    def to_dict(self) -> dict:
        return {
            "course_name": self.course_name,
            "course_text": self.course_location,
            "course_id": self.course_location,
        }
    
    def get_name(self) -> str:
        if self.course_text is None:
            return self.course_name.replace('_', ' ')
        elif '\n\n' not in self.course_text:
            return self.course_name.replace('_', ' ')
        else:
            return self.course_text.split('\n\n')[0]
        
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
