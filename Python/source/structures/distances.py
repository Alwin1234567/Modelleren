from source.locations import Location
from pandas import DataFrame
from typing import Set, List
from enum import Enum, auto
import numpy as np

class Status(Enum):
    PREPARING = auto()
    CALCULATING = auto()
    FINISHED = auto()

class Distances:
    
    def __init__(self) -> None:
        self._locations: Set[Location] = []
        self._distances = DataFrame()
        self._status = Status.PREPARING


    def add_location(self, location: Location) -> None:
        self._locations.add(location)
    
    def generate_distances(self) -> None:
        if self._status == Status.CALCULATING:
            raise Exception("Distances are already being calculated")
        elif self._status == Status.FINISHED:
            raise Exception("Distances are already calculated")
        elif self._status != Status.PREPARING:
            raise Exception("Distances are in an unknown state")
        self._status = Status.CALCULATING

        location_names = [location.name for location in self._locations]
        self._distances = DataFrame(index=location_names, columns=location_names)
        self._load_stored_distances()
        missing_distances = self._determine_missing_distances()
        if missing_distances:
            self._determine_distances(missing_distances)
        
        if not self._check_complete():
            raise Exception("Distances are not complete")
        self._status = Status.FINISHED

    def _load_stored_distances(self) -> None:
        if self._status != Status.CALCULATING:
            raise Exception("Distances are not being calculated")
        # Load stored distances from file

    def _determine_missing_distances(self) -> List[(Location, Location)]:
        if self._status != Status.CALCULATING:
            raise Exception("Distances are not being calculated")
        missing_distances = self._distances.isna().stack()
        missing_distances = missing_distances[missing_distances].index.tolist()
        missing_distances = [(row, col) for row, col in missing_distances if row != col]
        return missing_distances

    def _determine_distances(self, missing_distances: List[(Location, Location)]) -> None:
        # use OSRM to determine distances
        pass

    def _check_complete(self) -> bool:
        if self._status != Status.CALCULATING:
            raise Exception("Distances are not being calculated")
        # Mask the diagonal values
        mask = np.eye(self._distances.shape[0], dtype=bool)
        masked_distances = self._distances.mask(mask)

        # Check for None values excluding the diagonal
        return masked_distances.isna().any().any()


class distance_time:
    
    def __init__(self) -> None:
        self.distance = None
        self.time = None

    def get_distance(self, coordinates) -> None:
        pass
