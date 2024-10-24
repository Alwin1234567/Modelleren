from .location import Location, Coordinates, Location_type
from source.structures import Vraag

class Ziekenhuis(Location):
    
    def __init__(self, name: str, coordinates: Coordinates, wegbrengen: list, ophalen: list) -> None:
        super().__init__(coordinates, name, Location_type.ZIEKENHUIS)
        self._vraag_ophalen = Vraag(ophalen)
        self._vraag_wegbrengen = Vraag(wegbrengen)
    
    @property
    def vraag_ophalen(self):
        return self._vraag_ophalen
    
    @property
    def vraag_wegbrengen(self):
        return self._vraag_wegbrengen 
