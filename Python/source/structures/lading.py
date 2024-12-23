from enum import Enum, auto
import math
from source.constants import Constants

class Auto_type(Enum):
    BAKWAGEN = auto()
    BESTELBUS = auto()

class Bak_kar_voorkeur(Enum):
    BAK = auto()
    KAR = auto()

class Lading_bak_kar():
    """
    Een class die de lading in de benodigde vorm (sets, bakken of karren) teruggeeft.

    Properties:
        aantal_sets: De lading in het aantal instrumentensets.
        voorkeur: De voorkeur van het ziekenhuis voor een levering in bakken of karren.
        orthopedic: Het soort instrumenten. Orthopedische instrumentesets zijn groter dan andere sets.
    """
    def __init__(self, aantal_sets: int, voorkeur: Bak_kar_voorkeur, orthopedic = False):
        self._aantal_sets = aantal_sets
        self._voorkeur = voorkeur
        self._orthopedic = orthopedic
    
    def aantal(self, auto_type: Auto_type) -> int:
        """
        Stelt de voorkeur voor bakken of karren in.

        Parameters:
            auto_type (Auto_type): De auto waarmee gereden wordt.

        Returns:
            int: Het aantal bakken of karren dat nodig is voor het aantal instrumentensets afhankelijk van het type auto
        """
        if auto_type == Auto_type.BAKWAGEN:
            return self.aantal_karren
        elif auto_type == Auto_type.BESTELBUS:
            return self.aantal_bakken
        else:
            raise ValueError(f"Het autotype {auto_type} is onbekend.")
    
    @property
    def aantal_sets(self):
        """
        Geeft het aantal instrumentensets.
        """
        return self._aantal_sets

    @property
    def aantal_bakken(self) -> int:
        """
        Geeft het aantal bakken dat nodig is voor het aantal instrumentensets.
        """
        if self._voorkeur == Bak_kar_voorkeur.KAR:
            raise ValueError("Een ziekenhuis met een kar-voorkeur, kan geen levering in bakken krijgen")
        if self._orthopedic:
            return math.ceil(self._aantal_sets/(Constants.capaciteit_bak_kar(self._voorkeur)/2))
        return math.ceil(self._aantal_sets/Constants.capaciteit_bak_kar(self._voorkeur))
    
    @property
    def aantal_karren(self) -> int:
        """
        Geeft het aantal karren dat nodig is voor het aantal instrumentensets.
        Bij een voorkeur voor bakken, wordt het aantal kar-plekken dat ingenomen wordt door het aantal bakken gegeven.
        """
        if self._voorkeur == Bak_kar_voorkeur.BAK:
            return math.ceil(self.aantal_bakken/Constants.BAKKEN_PER_KAR)
        return math.ceil(self._aantal_sets/Constants.capaciteit_bak_kar(self._voorkeur))
    
    @property
    def laadtijd(self) -> float:
        """
        Geeft de tijd die het kost om het aantal karren of bakken uit te laden.
        """
        if self._voorkeur == Bak_kar_voorkeur.KAR:
            return Constants.tijdsduur_in_en_uitladen(self._voorkeur) * self.aantal_karren
        elif self._voorkeur == Bak_kar_voorkeur.BAK:
            return Constants.tijdsduur_in_en_uitladen(self._voorkeur) * self.aantal_bakken
    
    @property
    def voorkeur_bak_kar(self):
        """
        Geeft de voorkeur voor bakken of karren.
        """
        return self._voorkeur
    
    def set_voorkeur(self, voorkeur: Bak_kar_voorkeur):
        """
        Stelt de voorkeur voor bakken of karren in.

        Parameters:
            voorkeur (Bak_kar_voorkeur): De voorkeur voor bakken of karren van het ziekenhuis.
        """
        self._voorkeur = voorkeur
