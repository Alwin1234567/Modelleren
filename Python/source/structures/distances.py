from .status import Status
from .coordinates import Coordinates
from .maps import Maps
from source.locations import Location
from source.constants import Constants
from pandas import DataFrame
from typing import Set, List, Tuple
from enum import Enum, auto
import numpy as np
import requests
from warnings import warn

class Distances:
    """
    Een class om afstanden tussen locaties te beheren en te berekenen.
    """
    
    def __init__(self) -> None:
        """
        Initialiseer een nieuwe instantie van de Distances klasse.
        """
        self._locations: Set[Location] = []
        self._distances = DataFrame()
        self._status = Status.PREPARING


    def add_location(self, location: Location) -> None:
        """
        Voeg een locatie toe aan de set van locaties.

        Parameters:
            location (Location): De locatie die moet worden toegevoegd.
        """
        self._locations.add(location)
    
    def generate_distances(self) -> None:
        """
        Genereer de afstanden tussen alle toegevoegde locaties.

        Raises:
            Exception: Als de afstanden al worden berekend of al zijn berekend.
        """
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
        """
        Laad opgeslagen afstanden uit een bestand.

        Raises:
            Exception: Als de afstanden niet worden berekend.
        """
        if self._status != Status.CALCULATING:
            raise Exception("Distances are not being calculated")
        # Load stored distances from file

    def _determine_missing_distances(self) -> List[Tuple[Location, Location]]:
        """
        Bepaal de ontbrekende afstanden tussen locaties.
    
        Returns:
            missing_distances (List[Tuple[Location, Location]]): Een lijst van ontbrekende afstanden.
    
        Raises:
            Exception: Als de afstanden niet worden berekend.
        """
        if self._status != Status.CALCULATING:
            raise Exception("Distances are not being calculated")
        missing_distances = self._distances.isna().stack()
        missing_distances = missing_distances[missing_distances].index.tolist()
        missing_distances = [(row, col) for row, col in missing_distances if row != col]
        return missing_distances

    def _determine_distances(self, missing_distances: List[Tuple[Location, Location]]) -> None:
        """
        Bepaal de afstanden voor de ontbrekende locaties.

        Parameters:
            missing_distances (List[Tuple[Location, Location]]): Een lijst van ontbrekende afstanden.
        """
        if not Maps.is_enabled():
            self._activate_maps()
        for start, end in missing_distances:
            url = f"{Constants.MAPS_URL}?{start.coordinates.OSMR_str}&{end.coordinates.OSMR_str}&profile={Constants.MAPS_PARAMS['profile']}&locale={Constants.MAPS_PARAMS['locale']}&calc_points={Constants.MAPS_PARAMS['calc_points']}"
            response = requests.get(url)
            result = Distance_time(1e10, 1e10)
            if response.status_code == 200:
                data = response.json()
                if 'paths' in data and len(data['paths']) > 0:
                    path = data['paths'][0]
                    distance: float = path['distance']/1000  # Distance in kilometers
                    time: float = path['time']/1000/60  # Time in minutes
                    result = Distance_time(distance, time)
                else:
                    warn(f"No route found between {start} and {end}")
            self._distances.loc[start.name, end.name] = result
        
    def _check_complete(self) -> bool:
        """
        Controleer of alle afstanden zijn berekend.

        Returns:
            bool: True als alle afstanden zijn berekend, anders False.
        """
        if self._status != Status.CALCULATING:
            raise Exception("Distances are not being calculated")
        # Mask the diagonal values
        mask = np.eye(self._distances.shape[0], dtype=bool)
        masked_distances = self._distances.mask(mask)

        # Check for None values excluding the diagonal
        return masked_distances.isna().any().any()
    
    def _activate_maps(self) -> None:
        pass

    def _deactivate_maps(self) -> None:
        pass


class Distance_time:
    """
    Een class om de afstand en tijd tussen twee locaties te beheren.
    """

    def __init__(self, distance: float, time: float) -> None:
        """
        Initialiseer een nieuwe instantie van de Distance_time klasse.

        Parameters:
            distance (float): De afstand tussen twee locaties in kilometers.
            time (float): De tijd tussen twee locaties in minuten.
        """
        self._distance = distance
        self._time = time

    @property
    def distance(self) -> float:
        """
        Haal de afstand op.

        Returns:
            float: De afstand tussen twee locaties in kilometers.
        """
        return self._distance

    @property
    def time(self) -> float:
        """
        Haal de tijd op.

        Returns:
            float: De tijd tussen twee locaties in minuten.
        """
        return self._time

    
