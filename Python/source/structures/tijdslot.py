from datetime import time
from typing import Union, Tuple
from warnings import warn
from .long_time import Long_time

class Tijdslot:
    """
    Een class die een tijdslot voor een pickup of delivery representeert.
    """
    def __init__(self, start: Long_time, eind: Long_time) -> None:
        """
        Creëer een nieuw tijdslot.
        """
        if eind < start:
            raise ValueError("De eindtijd van een tijdslot kan niet voor de starttijd liggen.")
        self._start = start
        self._eind = eind

    def is_in_tijdvak(self, tijd: Long_time) -> bool:
        """
        Controleer of een tijd in het tijdvak ligt.
        
        Parameters:
            tijd (Long_time): De tijd die gecontroleerd moet worden.
        
        Returns:
            bool: True als de tijd in het tijdvak ligt, anders False.
        """
        return self._start <= tijd <= self._eind
    
    def overlap(self, tijdslot: 'Tijdslot') -> bool:
        """
        Controleer of twee tijdsloten overlappen.
        
        Parameters:
            tijdslot (Tijdslot): Het tijdslot dat gecontroleerd moet worden.
        
        Returns:
            bool: True als de tijdsloten overlappen, anders False.
        """
        return self.is_in_tijdvak(tijdslot.starttijd) or self.is_in_tijdvak(tijdslot.eindtijd)

    def __len__(self) -> int:
        """
        Bereken de lengte van het tijdslot in uren.
        
        Returns:
            float: De lengte van het tijdslot in uren.
        """
        return int(float(self._eind) - float(self._start))


    @property
    def starttijd(self):
        return self._start
    
    @property
    def eindtijd(self):
        return self._eind
    
    @property
    def dag(self):
        return self._dag
    
    @property
    def length(self) -> float:
        return float(self._eind) - float(self._start)
