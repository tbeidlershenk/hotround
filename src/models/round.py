from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.event import Event
from models.score import Score

class Round(Base):
    __tablename__ = 'Rounds'
    round_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('Events.event_id', ondelete='CASCADE'), nullable=False)
    layout_id = Column(Integer, ForeignKey('Layouts.layout_id', ondelete='CASCADE'), nullable=False)
    round_number = Column(Integer, nullable=False)
    num_players = Column(Integer, nullable=False)
    high_rating = Column(Integer, nullable=False)
    low_rating = Column(Integer, nullable=False)
    par_rating = Column(Integer, nullable=False)
    stroke_value = Column(DECIMAL(5, 2), nullable=False)
    event = relationship('Event', back_populates='rounds', foreign_keys=[event_id])
    layout = relationship('Layout', back_populates='round', uselist=False)
    scores = relationship('Score', back_populates='round')

    def to_dict(self) -> dict:
        return {
            "round_number": self.round_number,
            "num_players": self.num_players,
            "high_rating": self.high_rating,
            "low_rating": self.low_rating,
            "par_rating": self.par_rating,
            "stroke_value": self.stroke_value,
            "event": self.event.to_dict(),
            "layout": self.layout.to_dict(),
            "scores": [x.to_dict() for x in self.scores]
        }
    