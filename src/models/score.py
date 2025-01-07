from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Score(Base):
    __tablename__ = 'Scores'
    score_id = Column(Integer, primary_key=True, autoincrement=True)
    round_id = Column(Integer, ForeignKey('Rounds.round_id', ondelete='CASCADE'), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    hole_scores = Column(String(200), nullable=True) 
    round = relationship('Round', back_populates='scores', foreign_keys=[round_id])

    def to_dict(self) -> dict:
        return {
            "rating": self.rating,
            "score": self.score,
            "hole_scores": self.hole_scores,
        }
