from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from models.base import Base
from itertools import groupby
import numpy as np
from util.strings import to_pdgalive_link
from logger import logger

class Layout(Base):
    __tablename__ = 'Layouts'
    layout_id = Column(Integer, primary_key=True, autoincrement=True)
    round_id = Column(Integer, ForeignKey('Rounds.round_id', ondelete='CASCADE'), nullable=False)
    layout_name = Column(String(200), nullable=False)
    num_holes = Column(Integer, nullable=False)
    # Comma separated list of distances for each hole
    distances = Column(String(200), nullable=True)
    # Comma separated list of pars for each hole
    pars = Column(String(200), nullable=False)
    total_par = Column(Integer, nullable=False)
    total_distance = Column(Integer, nullable=True)
