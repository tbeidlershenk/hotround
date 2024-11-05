from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from models.base import Base
from itertools import groupby
import numpy as np
from util.strings import to_pdgalive_link

class Round(Base):
    __tablename__ = 'Rounds'
    round_id = Column(Integer, primary_key=True, autoincrement=True)
    layout_name = Column(String(200), nullable=False)
    round_number = Column(Integer, nullable=False)
    num_players = Column(Integer, nullable=False)
    layout_par = Column(Integer, nullable=False)
    layout_hole_distances = Column(String(200), nullable=False)
    layout_total_distance = Column(Integer, nullable=False)
    high_rating = Column(Integer, nullable=False)
    low_rating = Column(Integer, nullable=False)
    par_rating = Column(Integer, nullable=False)
    stroke_value = Column(DECIMAL(5, 2), nullable=False)
    event_id = Column(Integer, ForeignKey('Events.event_id', ondelete='CASCADE'), nullable=False)

class Layout:
    def __init__(self, layout_hole_distances: str, layout_total_distance: int, layout_par: int, layout_names: list[str], rounds_used: list[Round]):
        self.layout_hole_distances = layout_hole_distances
        self.layout_total_distance = layout_total_distance
        self.layout_par = layout_par
        self.layout_names = layout_names
        self.rounds_used = rounds_used

    def par_rating(self) -> int:
        return int(np.mean([x.par_rating for x in self.rounds_used]))
    
    def score_rating(self, score: int) -> int:
        par_rating = self.par_rating()
        stroke_value = np.mean([x.stroke_value for x in self.rounds_used])
        return int(par_rating - (score * stroke_value))
    
    def hole_distances(self, columns: int = 3) -> list[str]:
        hole_distances = self.layout_hole_distances.split(', ')
        holes_per_column = (len(hole_distances) // columns)
        holes_per_column += 1 if len(hole_distances) % columns != 0 else 0
        hole_columns = []
        for c in range(columns):
            start = c*holes_per_column
            end = (c+1)*holes_per_column
            holes = hole_distances[c*holes_per_column:(c+1)*holes_per_column]
            hole_columns.append('\n'.join([f"H{start+hole+1}: {dist}" for hole, dist in enumerate(holes)]))
        return hole_columns
    
    def course_metadata(self) -> str:
        return (f"Total distance {self.layout_total_distance}, Par {self.layout_par}\n"
                f"Calculated using [{len(self.rounds_used)} rounds]({to_pdgalive_link(self.rounds_used[0])})\n")

def remove_distance_outliers(rounds: list[Round], threshold: int):
    distances = np.array([round.layout_total_distance for round in rounds])
    upper_quartile = np.percentile(distances, 75)
    lower_quartile = np.percentile(distances, 25)
    iqr = (upper_quartile - lower_quartile) * threshold
    quartile_set = (lower_quartile - iqr, upper_quartile + iqr)
    filtered_rounds = [round for round in rounds if quartile_set[0] <= round.layout_total_distance <= quartile_set[1]]
    return filtered_rounds

def group_comparable_rounds(rounds: list[Round], threshold: int = 300) -> list[Layout]:
    """
    Groups rounds into comparable layouts based on their hole distances, total distance, and par.
    Args:
        rounds (list[Round]): A list of Round objects to be grouped.
    Returns:
        list[Layout]: A list of Layout objects, each representing a group of comparable rounds.
    """
    

    layout_groups = []
    for key, group in groupby(rounds, key=lambda r: r.layout_par):
        group_list = remove_distance_outliers(list(group), threshold)
        layout_groups.append(
            Layout(
                "",
                int(np.mean([r.layout_total_distance for r in group_list])),
                key, 
                list(set([r.layout_name for r in group_list])), 
                group_list
            )
        )
    layout_groups.sort(key=lambda x: len(x.rounds_used), reverse=True)
    return layout_groups
