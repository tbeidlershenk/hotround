from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from models.base import Base
from itertools import groupby
import numpy as np
from models.layout import Layout
from util.strings import to_pdgalive_link
from logger import logger

class Round(Base):
    __tablename__ = 'Rounds'
    round_id = Column(Integer, primary_key=True, autoincrement=True)
    round_number = Column(Integer, nullable=False)
    num_players = Column(Integer, nullable=False)
    high_rating = Column(Integer, nullable=False)
    low_rating = Column(Integer, nullable=False)
    par_rating = Column(Integer, nullable=False)
    stroke_value = Column(DECIMAL(5, 2), nullable=False)
    event_id = Column(Integer, ForeignKey('Events.event_id', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {
            "round_id": self.round_id,
            "round_number": self.round_number,
            "num_players": self.num_players,
            "high_rating": self.high_rating,
            "low_rating": self.low_rating,
            "par_rating": self.par_rating,
            "stroke_value": self.stroke_value,
            "event_id": self.event_id
        }
    