from .location import Location, Coordinates, Location_type
from source.structures import Taak
from datetime import time

class Ziekenhuis(Location):
    
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, Location_type.ZIEKENHUIS, **kwargs)
        self._taken: list[Taak] = []

    def add_taak(self, taak: Taak):
        self._taken.append(taak)

    @property
    def taken(self):
        return self._taken
