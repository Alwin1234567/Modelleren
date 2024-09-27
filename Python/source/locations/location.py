from enum import Enum, auto
from source.structures import Coordinates

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
