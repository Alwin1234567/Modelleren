from enum import Enum, auto
from source.structures import Coordinates, ID

class Location_type(Enum):
    HUB = auto()
    ZIEKENHUIS = auto()

class Location:
    def __init__(self, coordinates: Coordinates, name: str, type: Location_type) -> None:
        self._coordinates = coordinates
        self._name = name
        self._type = type
        self._id = ID()
    
    def __str__(self) -> str:
        return f"{self._name} ({self._coordinates})"
    
    @property
    def coordinates(self):
        return self._coordinates
    
    @property
    def name(self):
        return self._name
    
    @property
    def type(self):
        return self._type
    
    @property
    def id(self):
        return self._id
