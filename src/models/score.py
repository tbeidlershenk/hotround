from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from models.base import Base
from itertools import groupby
import numpy as np
from server import rating
from util.strings import to_pdgalive_link
from logger import logger

class Score(Base):
    __tablename__ = 'Scores'
    score_id = Column(Integer, primary_key=True, autoincrement=True)
    round_id = Column(Integer, ForeignKey('Rounds.round_id', ondelete='CASCADE'), nullable=False)
    rating = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    # Comma separated list of scores for each hole
    hole_scores = Column(String(200), nullable=True) 
