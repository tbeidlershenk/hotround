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
    def __init__(self, layout_hole_distances: list[int], layout_total_distance: int, layout_par: int, layout_names: list[str], rounds_used: list[Round]):
        self.layout_hole_distances = layout_hole_distances
        self.layout_total_distance = layout_total_distance
        self.layout_par = layout_par
        self.layout_names = layout_names
        self.rounds_used = rounds_used
    
    def score_rating(self, score: int) -> dict:
        par_ratings = [x.par_rating for x in self.rounds_used]
        par_rating = int(np.mean(par_ratings))
        stroke_value = np.mean([x.stroke_value for x in self.rounds_used])
        return {
            "rating": int(par_rating - (score * stroke_value)),
            "error": int(np.std(par_ratings))
        }

    def layouts_used(self) -> list[str]:
        self.rounds_used.sort(key=lambda x: x.event_id)
        grouped_layouts: groupby[int, list[Round]] = groupby(self.rounds_used, key=lambda r: r.event_id)        
        return [f"[{list(rounds)[0].layout_name}]({to_pdgalive_link(event_id)})" for event_id, rounds in grouped_layouts]
    
    def hole_distances(self, columns: int = 3) -> list[str]:
        holes_per_column = (len(self.layout_hole_distances) // columns)
        holes_per_column += 1 if len(self.layout_hole_distances) % columns != 0 else 0
        hole_columns = []
        for c in range(columns):
            start = c*holes_per_column
            holes = self.layout_hole_distances[c*holes_per_column:(c+1)*holes_per_column]
            hole_columns.append('\n'.join([f"H{start+hole+1}: {dist}" for hole, dist in enumerate(holes)]))
        return hole_columns
    
    def course_metadata(self) -> str:
        return (f"Par {self.layout_par}, Distance {self.layout_total_distance} feet")

def remove_distance_outliers(rounds: list[Round], threshold: int):
    distances = np.array([round.layout_total_distance for round in rounds])
    upper_quartile = np.percentile(distances, 75)
    lower_quartile = np.percentile(distances, 25)
    iqr = (upper_quartile - lower_quartile) * threshold
    quartile_set = (lower_quartile - iqr, upper_quartile + iqr)
    filtered_rounds = [round for round in rounds if quartile_set[0] <= round.layout_total_distance <= quartile_set[1]]
    return filtered_rounds

def remove_rating_outliers(rounds: list[Round], threshold: int = 5):
    ratings = np.array([round.par_rating for round in rounds])
    upper_quartile = np.percentile(ratings, 75)
    print(upper_quartile)
    lower_quartile = np.percentile(ratings, 25)
    iqr = (upper_quartile - lower_quartile) * threshold
    quartile_set = (lower_quartile - iqr, upper_quartile + iqr)
    filtered_rounds = [round for round in rounds if quartile_set[0] <= round.par_rating <= quartile_set[1]]
    return filtered_rounds

def group_comparable_rounds(rounds: list[Round], threshold: int = 0.5) -> list[Layout]:
    """
    Groups rounds into comparable layouts based on their hole distances, total distance, and par.
    Args:
        rounds (list[Round]): A list of Round objects to be grouped.
    Returns:
        list[Layout]: A list of Layout objects, each representing a group of comparable rounds.
    """
    layout_groups: list[Layout] = []
    rounds.sort(key=lambda x: x.layout_par)
    for key, group in groupby(rounds, key=lambda r: int(r.layout_par)):
        group_list = remove_distance_outliers(list(group), threshold)
        str_hole_dists = [r.layout_hole_distances.split(', ') for r in group_list]
        hole_dists = [[int(x) for x in y] for y in str_hole_dists]
        averaged_hole_dists = []
        for i in range(len(hole_dists[0])):
            average_hole_dist = int(np.mean([hole_dists[j][i] for j in range(len(hole_dists))]))
            averaged_hole_dists.append(average_hole_dist)

        layout = Layout(
            averaged_hole_dists,
            int(np.mean([r.layout_total_distance for r in group_list])),
            key, 
            list(set([r.layout_name for r in group_list])), 
            group_list
        )

        # bit of a hack for now. add DB constraints to prevent wild outliers
        if layout.score_rating(0)['error'] > 100:
            continue
        # else, add it
        layout_groups.append(layout)

    layout_groups.sort(key=lambda x: len(x.rounds_used), reverse=True)
    return layout_groups
