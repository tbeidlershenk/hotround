from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from models.base import Base
from itertools import groupby
import numpy as np
from models.round import Round
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

class AggregateLayout:
    def __init__(self, layouts_rounds: list[tuple[Layout, Round]]):
        """
        Generates an aggregate layout by averaging a list of layouts.
        Assumes that the list is non-empty and layouts have valid data.
        """
        self.layouts = [x[0] for x in layouts_rounds]
        self.rounds = [x[1] for x in layouts_rounds]
        self.num_layouts = len(self.layouts)
        self.distances = self.averaged_distances()
        self.pars = [int(x) for x in self.layouts[0].pars]
        self.total_distance = int(np.mean([x.total_distance for x in self.layouts]))
        self.total_par = self.layouts[0].total_par
        self.num_holes = self.layouts[0].num_holes
        self.layout_names = [x.layout_name for x in self.layouts]
        self.layout_tokens = self.tokenize_layout_names()
        self.descriptive_name = self.get_descriptive_name()
        self.par_rating = int(np.mean([x.par_rating for x in self.rounds]))
        self.stroke_value = int(np.mean([x.stroke_value for x in self.rounds]))
        

    def to_dict(self) -> dict:
        return {
            "distances": self.distances,
            "total_distance": self.total_distance,
            "pars": self.pars,
            "total_par": self.total_par,
            "num_holes": self.num_holes,
            "layout_names": self.layout_names,
            "layout_tokens": self.layout_tokens,
            "descriptive_name": self.descriptive_name,
            "par_rating": self.par_rating,
            "stroke_value": self.stroke_value
        }

    def averaged_distances(self) -> list[int]:
        str_distances = [x.distances.split(', ') for x in self.layouts_used]
        int_distances = [[int(x) for x in y] for y in str_distances]
        distances = []
        for i in range(self.num_holes):
            averaged_distance = int(np.mean([int_distances[j][i] for j in range(self.num_layouts)]))
            distances.append(averaged_distance)
        return distances

    def get_descriptive_name(self) -> str:
        filtered_tokens = [token for token in self.layout_tokens if len(token) > 2]
        filtered_tokens = [token for token in filtered_tokens if not token.isnumeric()]
        return ', '.join(filtered_tokens[0:5])
    
    def tokenize_layout_names(self) -> list[str]:
        tokens = []
        frequencies = {}
        for name in self.layout_names:
            tokens.extend(name.lower().split(' '))
        for token in tokens:
            if token in frequencies:
                frequencies[token] += 1
            else:
                frequencies[token] = 1
        sorted_frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
        sorted_tokens = [token for (token, _) in sorted_frequencies]
        logger.info(sorted_frequencies)
        logger.info(sorted_tokens)
        return sorted_tokens

    def hole_distances(self, columns: int = 3) -> list[str]:
        holes_per_column = (len(self.distances) // columns)
        holes_per_column += 1 if len(self.distances) % columns != 0 else 0
        hole_columns = []
        for c in range(columns):
            start = c*holes_per_column
            holes = self.distances[c*holes_per_column:(c+1)*holes_per_column]
            hole_columns.append('\n'.join([f"H{start+hole+1}: {dist}" for hole, dist in enumerate(holes)]))
        return hole_columns
    
    def score_rating(self, score: int) -> int:
        return int(self.par_rating - (score * self.stroke_value)),
    
    def calculate_variance(self) -> int:
        distances = [x.total_distance for x in self.layouts]
        return int(np.std(distances))
    
    def course_metadata(self) -> str:
        return (f"Par {self.total_par}, Distance {self.total_distance} feet")
    
    def layout_links(self) -> list[str]:
        return []

def filter_layouts(layouts_rounds: list[tuple[Layout, Round]]):
    """
    Filters out layouts that do not have necessary data to be aggregated
    Args:
        layouts (list[Layout])
    Returns:
        list[Layout]: A list of Layout objects with complete distances, pars, total distance, etc.
    """
    filtered_layouts = []
    for layout_round in layouts_rounds:
        layout = layout_round[0]
        hole_distances: list[str] = layout.distances.split(',')
        pars: list[str] = layout.pars.split(',')
        if len(hole_distances) != layout.num_holes:
            continue
        if len(pars) != layout.num_holes:
            continue
        if not all(hole_distances, lambda x: x.isdigit()):
            continue
        if not all(pars, lambda x: x.isdigit()):
            continue
        filtered_layouts.append(layout_round)
    return filtered_layouts
    
def aggregate_layouts(layouts_rounds: list[tuple[Layout, Round]], threshold: int = 0.5) -> list[AggregateLayout]:
    """
    Groups rounds into comparable layouts based on their hole distances, total distance, and par.
    Args:
        rounds (list[Round]): A list of Round objects to be grouped.
    Returns:
        list[Layout]: A list of Layout objects, each representing a group of comparable rounds.
    """
    layout_groups: list[AggregateLayout] = []

    # BETTER SOLUTION
    # 1. remove layouts without distance data
    # 2. group layouts based on pars
    # 3. remove distance outliers
    # 

    layouts_rounds = filter_layouts(layouts_rounds)
    layouts_rounds.sort(key=lambda x: x[0].pars)
    for _, group in groupby(layouts_rounds, key=lambda x: x[0].pars):
        group_list = list(group)

        # TODO: remove distance outliers

        if len(group_list) == 0:
            continue

        layout = AggregateLayout(group_list)
        layout_groups.append(layout)

    layout_groups.sort(key=lambda x: len(x.num_layouts), reverse=True)
    return layout_groups

