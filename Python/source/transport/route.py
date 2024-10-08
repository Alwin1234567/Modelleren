from enum import Enum, auto
from source.locations import Location
from source.structures import Status, Distances, ID
from warnings import warn
from typing import List

class Route_type(Enum):
    AVOND = auto()
    OCHTEND = auto()

class Route:

    # destances will be a reference to the relevant distances object
    def __init__(self, route_type: Route_type, start: Location, distances: Distances) -> None:
        self._distances = distances
        if self._distances.status != Status.FINISHED:
            raise ValueError("Distances object is not finished")
        self._route_type = route_type
        self._start = start
        self._locations: List[Location] = []
        self._status = Status.PREPARING
        self._id = ID()
    
    def add_location(self, location: Location) -> None:
        """
        Voeg een locatie toe aan de route.
        
        Parameters:
            location (Location): De locatie die moet worden toegevoegd.
        
        Raises:
            ValueError: Als de route niet in de preparing status is.
            ValueError: Als de locatie niet in de distances object zit.
            Warning: Als de locatie al in de route zit.
        """
        if self._status != Status.PREPARING:
            raise ValueError("Route is not in preparing state")
        if not self._distances.has_location(location):
            raise ValueError("Location is not in distances object")
        if location in set(self._locations):
            warn("Location is already in route")
        self._locations.append(location)
    
    def copy(self) -> 'Route':
        """
        Maak een kopie van de route.
        
        Returns:
            Route: Een kopie van de route.
        """
        new_route = Route(self._route_type, self._start, self._distances)
        new_route._locations = self._locations.copy()
        new_route._status = self._status
        return new_route
    
    @property
    def status(self) -> Status:
        return self._status
    
    @property
    def locations(self) -> List[Location]:
        return self._locations
    
    @property
    def route_type(self) -> Route_type:
        return self._route_type
    
    @property
    def start(self) -> Location:
        return self._start
    
    @property
    def total_distance(self) -> float:
        """
        Bereken de totale afstand van de route.
        
        Returns:
            float: De totale afstand van de route.
        """
        total_distance = 0
        total_distance += self._distances.get_distance(self._start, self._locations[0])
        for i in range(len(self._locations) - 1):
            total_distance += self._distances.get_distance(self._locations[i], self._locations[i + 1])
        total_distance += self._distances.get_distance(self._locations[-1], self._start)
        return total_distance

    @property
    def total_time(self) -> float:
        """
        Bereken de totale tijd van de route.
        
        Returns:
            float: De totale tijd van de route.
        """
        total_time = 0
        total_time += self._distances.get_time(self._start, self._locations[0])
        for i in range(len(self._locations) - 1):
            total_time += self._distances.get_time(self._locations[i], self._locations[i + 1])
        total_time += self._distances.get_time(self._locations[-1], self._start)
        return total_time

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def cost(self) -> float:
        """
        Bereken de kosten van de route.
        
        Returns:
            float: De kosten van de route.
        """
        return 0.0
