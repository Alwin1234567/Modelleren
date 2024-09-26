from enum import Enum, auto

class Coordinates:
    def __init__(self, lat, lon) -> None:
        self._lat = lat
        self._lon = lon
    
    def __str__(self) -> str:
        return f"({self.lat}, {self.lon})"

    @property
    def lat(self):
        return self._lat
    
    @property
    def lon(self):
        return self._lon
    
    @property
    def coordinates(self):
        return (self.lat, self.lon)

class Location_type(Enum):
    HUB = auto()
    ZIEKENHUIS = auto()

class Location:
    def __init__(self, coordinates: Coordinates, name: str, type: Location_type) -> None:
        self._coordinates = coordinates
        self._name = name
        self._type = type
    
    @property
    def coordinates(self):
        return self._coordinates
    
    @property
    def name(self):
        return self._name
    
    @property
    def type(self):
        return self._type
