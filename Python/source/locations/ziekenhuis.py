from .location import Location, Coordinates, Location_type
from source.structures import Vraag
from datetime import time

class Ziekenhuis(Location):
    
    def __init__(self, name: str, wegbrengen: list, ophalen: list) -> None:
        super().__init__(name, Location_type.ZIEKENHUIS)
        self._vraag_ophalen = Vraag(ophalen)
        self._vraag_wegbrengen = Vraag(wegbrengen)
    
    @property
    def vraag_ophalen(self):
        return self._vraag_ophalen
    
    @property
    def vraag_wegbrengen(self):
        return self._vraag_wegbrengen 
    
    @property
    def tijdvak(self):
        return (time(6, 0), time(20, 0))
