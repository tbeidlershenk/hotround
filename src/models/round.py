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

class AggregateLayout:
    def __init__(self, rounds_used: list[Round], layouts_used: list[Layout]):
        self.layouts_used = layouts_used
        self.rounds_used = rounds_used

    def score_rating(self, score: int) -> dict:
        par_ratings = [x.par_rating for x in self.rounds_used]
        par_rating = int(np.mean(par_ratings))
        stroke_value = np.mean([x.stroke_value for x in self.rounds_used])
        return {
            "rating": int(par_rating - (score * stroke_value)),
            "error": int(np.std(par_ratings))
        }

    def layout_links(self) -> list[str]:
        self.rounds_used.sort(key=lambda x: x.event_id)
        grouped_layouts: groupby[int, list[Round]] = groupby(self.rounds_used, key=lambda r: r.event_id)        
        return [f"[{list(rounds)[0].layout_name}]({to_pdgalive_link(event_id)})" for event_id, rounds in grouped_layouts]
    
    def layouts_to_url(self) -> list[dict]:
        self.rounds_used.sort(key=lambda x: x.event_id)
        grouped_layouts: groupby[int, list[Round]] = groupby(self.rounds_used, key=lambda r: r.event_id)        
        return [{
            "layout_name": list(rounds)[0].layout_name, 
            "pdga_live_link": to_pdgalive_link(event_id)
        } for event_id, rounds in grouped_layouts]

    def hole_distances(self, columns: int = 3) -> list[str]:
        holes_per_column = (len(self.layout_hole_distances) // columns)
        holes_per_column += 1 if len(self.layout_hole_distances) % columns != 0 else 0
        hole_columns = []
        for c in range(columns):
            start = c*holes_per_column
            holes = self.layout_hole_distances[c*holes_per_column:(c+1)*holes_per_column]
            hole_columns.append('\n'.join([f"H{start+hole+1}: {dist}" for hole, dist in enumerate(holes)]))
        return hole_columns
    
    def calculate_variance(self) -> int:
        distances = [round.layout_total_distance for round in self.rounds_used]
        return int(np.std(distances))
    
    def course_metadata(self) -> str:
        return (f"Par {self.layout_par}, Distance {self.layout_total_distance} feet")
    
    def to_dict(self) -> dict:
        return {
            "layout_hole_distances": self.layout_hole_distances,
            "layout_total_distance": self.layout_total_distance,
            "layout_par": self.layout_par,
            "layout_names": self.layout_names,
            "rounds_used": [x.to_dict() for x in self.rounds_used]
        }

def remove_distance_outliers(rounds: list[Round], threshold: int) -> list:
    distances = np.array([round.layout_total_distance for round in rounds])
    upper_quartile = np.percentile(distances, 75)
    lower_quartile = np.percentile(distances, 25)
    iqr = (upper_quartile - lower_quartile) * threshold
    quartile_set = (lower_quartile - iqr, upper_quartile + iqr)
    filtered_rounds = [round for round in rounds if quartile_set[0] <= round.layout_total_distance <= quartile_set[1]]
    return filtered_rounds

def remove_rating_outliers(rounds: list[Round], threshold: int = 5) -> list:
    ratings = np.array([round.par_rating for round in rounds])
    upper_quartile = np.percentile(ratings, 75)
    print(upper_quartile)
    lower_quartile = np.percentile(ratings, 25)
    iqr = (upper_quartile - lower_quartile) * threshold
    quartile_set = (lower_quartile - iqr, upper_quartile + iqr)
    filtered_rounds = [round for round in rounds if quartile_set[0] <= round.par_rating <= quartile_set[1]]
    return filtered_rounds

def group_comparable_rounds(rounds: list[Round], threshold: int = 0.5) -> list[AggregateLayout]:
    """
    Groups rounds into comparable layouts based on their hole distances, total distance, and par.
    Args:
        rounds (list[Round]): A list of Round objects to be grouped.
    Returns:
        list[Layout]: A list of Layout objects, each representing a group of comparable rounds.
    """
    layout_groups: list[AggregateLayout] = []
    rounds.sort(key=lambda x: x.layout_par)
    for key, group in groupby(rounds, key=lambda r: int(r.layout_par)):
        group_list = list(group)
        group_list = remove_distance_outliers(group_list, threshold)
        if len(group_list) == 0:
            continue

        str_hole_dists = [r.layout_hole_distances.split(', ') for r in group_list if ',' in r.layout_hole_distances]
        hole_dists = [[int(x) for x in y] for y in str_hole_dists]
        averaged_hole_dists = []
        for i in range(len(hole_dists[0])):
            try:
                average_hole_dist = int(np.mean([hole_dists[j][i] for j in range(len(hole_dists))]))
                averaged_hole_dists.append(average_hole_dist)
            except:
                #literally hacks everywhere, ill fix this oneday
                continue

        layout = AggregateLayout(
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

    # also bit of a hack
    layout_groups = [layout for layout in layout_groups if layout.calculate_variance() <= 300]
    layout_groups.sort(key=lambda x: len(x.rounds_used), reverse=True)
    return layout_groups
