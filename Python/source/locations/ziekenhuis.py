from .location import Location, Location_type
from source.structures import Taak, Bak_kar_voorkeur

class Ziekenhuis(Location):
    
    def __init__(self, name: str, voorkeur: Bak_kar_voorkeur, **kwargs) -> None:
        super().__init__(name, Location_type.ZIEKENHUIS, **kwargs)
        self._taken: list[Taak] = []
        self._voorkeur = voorkeur

    def add_taak(self, taak: Taak) -> None:
        """
        Voeg een taak toe aan het ziekenhuis.

        Parameters:
            taak (Taak): De taak die aan het ziekenhuis moet worden toegevoegd
        """
        self._taken.append(taak)

    @property
    def taken(self):
        """
        Geef de taken die aan het ziekenhuis gekoppeld zijn.
        """
        return self._taken
    
    @property
    def voorkeur_bak_kar(self):
        """
        Geef de voorkeur van het ziekenhuis voor bakken of karren.
        """
        return self._voorkeur
