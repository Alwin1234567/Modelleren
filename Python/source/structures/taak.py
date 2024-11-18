from .tijdslot import Tijdslot
from .distances import Distances
from .long_time import Long_time
from .cost import Cost
from typing import TYPE_CHECKING, Optional
from datetime import time
from .id import ID
from source.constants import Constants
import numpy as np
from .lading import Lading_bak_kar, Auto_type

if TYPE_CHECKING:
    from source.locations import Ziekenhuis

class Taak:
    """
    Een class die een taak voorstelt die uitgevoerd moet worden door een voertuig.

    Properties:
        Tijdslot: De tijdslot van de taak.
        Ziekenhuis: Het ziekenhuis van de taak.
        Brengen: Het aantal instrumenten dat gebracht moet worden.
        Halen: Het aantal instrumenten dat gehaald moet worden.
        Halen_brengen: Het totaal aantal instrumenten dat gehaald en gebracht moet worden.
        Laadtijd: De laadtijd van de taak.
        Begintijd_taak: De begintijd van de taak.
        Eindtijd_taak: De eindtijd van de taak.
        ID: Het id van de taak.
        Has_ingeplande_tijd: Controleer of de taak een ingeplande tijd heeft.
        Returntijd: Het tijdvak waarin de opgehaalde instrumenten schoon terug bij het ziekenhuis moeten zijn.
    """

    def __init__(self,
                 tijdslot: Tijdslot,
                 ziekenhuis: "Ziekenhuis",
                 brengen: int = 0,
                 halen: int = 0,
                 returntijd: Tijdslot = Tijdslot(Long_time(7*24*60), Long_time(7*24*60))
                 ) -> None:
        """
        Creëer een nieuwe taak.
        """
        if brengen < 0 or halen < 0:
            raise ValueError("Het aantal brengen en halen kan niet negatief zijn.")
        if brengen == 0 and halen == 0:
            raise ValueError("Een taak moet minimaal brengen of halen.")
        self._tijdslot = tijdslot
        self._ingeplande_tijd: Optional[Long_time] = None
        self._ziekenhuis = ziekenhuis
        self._brengen = Lading_bak_kar(brengen, ziekenhuis.voorkeur_bak_kar)
        self._halen = Lading_bak_kar(halen, ziekenhuis.voorkeur_bak_kar)
        if not tijdslot.is_in_tijdvak(tijdslot.starttijd + self.laadtijd):
            raise ValueError("Het tijdslot moet lang genoeg zijn om te kunnen in- en uitladen")
        self._returntijd = returntijd
        self._id = ID()
    

    def cost_with_taak(self, taak: "Taak", distances: Distances, auto_type: Auto_type = Auto_type.BAKWAGEN, end = True) -> int:
        """
        Bereken de kosten van een taak tenopzichte van deze taak.

        Parameters:
            taak (Taak): De taak waarvan de kosten berekend moeten worden.
            distances (Distances): De afstanden matrix met daarin de locaties van de taken.
            end (bool): True als de meegegeven taak na de huidige taak komt.

        Returns:
            int: De kosten van de taak.
        """
        if not self.has_ingeplande_tijd:
            raise ValueError("De taak heeft geen ingeplande tijd.")
        if not distances.has_location(self.ziekenhuis) or not distances.has_location(taak.ziekenhuis):
            raise ValueError("De afstanden zijn niet bekend.")
        if end:
            distance = distances.get_distance(self.ziekenhuis, taak.ziekenhuis)
            time = distances.get_time(self.ziekenhuis, taak.ziekenhuis)
            earliest_time = self.eindtijd_taak + time
            if taak.has_ingeplande_tijd:
                if earliest_time > taak.begintijd_taak:
                    return np.inf
                time_cost = Cost.calculate_cost_time(self.eindtijd_taak.tijd, self.eindtijd_taak.difference(taak.begintijd_taak))
            else:
                if earliest_time > taak.tijdslot.eindtijd - taak.laadtijd:
                    return np.inf
                earliest_time = max(earliest_time, taak.tijdslot.starttijd)
                time_cost = Cost.calculate_cost_time(self.eindtijd_taak.tijd, self.eindtijd_taak.difference(earliest_time))
        else:
            distance = distances.get_distance(taak.ziekenhuis, self.ziekenhuis)
            time = distances.get_time(taak.ziekenhuis, self.ziekenhuis)
            latest_time = self.begintijd_taak - time
            if taak.has_ingeplande_tijd:
                if latest_time < taak.eindtijd_taak:
                    return np.inf
                time_cost = Cost.calculate_cost_time(taak.eindtijd_taak.tijd, taak.eindtijd_taak.difference(self.begintijd_taak))
            else:
                if latest_time < taak.tijdslot.starttijd + taak.laadtijd:
                    return np.inf
                latest_time = min(latest_time, taak.tijdslot.eindtijd)
                time_cost = Cost.calculate_cost_time(latest_time.tijd, latest_time.difference(self.begintijd_taak))

        if auto_type == Auto_type.BAKWAGEN:
            distance_cost = distance * Constants.PRIJS_PER_KM_BAKWAGEN
        else:
            distance_cost = distance * Constants.PRIJS_PER_KM_BESTELBUS
        return distance_cost + time_cost
    
    def __eq__(self, value: object) -> bool:
        """
        Controleer of twee taken gelijk zijn.
        """
        if not isinstance(value, Taak):
            return False
        return self.id == value.id


    @property
    def tijdslot(self) -> Tijdslot:
        """
        De tijdslot van de taak.
        """
        return self._tijdslot
    
    @property
    def ziekenhuis(self) -> "Ziekenhuis":
        """
        Het ziekenhuis van de taak.
        """
        return self._ziekenhuis
    
    @property
    def brengen(self) -> Lading_bak_kar:
        """
        Het aantal instrumenten dat gebracht moet worden.
        """
        return self._brengen
    
    @property
    def halen(self) -> Lading_bak_kar:
        """
        Het aantal instrumenten dat gehaald moet worden.
        """
        return self._halen
    
    @property
    def halen_brengen_sets(self) -> int:
        """
        Het totaal aantal instrumenten dat gehaald en gebracht moet worden.
        """
        return self._brengen.aantal_sets + self._halen.aantal_sets
    
    @property
    def has_brengen(self) -> bool:
        """
        Controleer of er instrumenten gebracht moeten worden.
        """
        return self._brengen.aantal_sets > 0
    
    @property
    def has_halen(self) -> bool:
        """
        Controleer of er instrumenten gehaald moeten worden.
        """
        return self._halen.aantal_sets > 0
    
    @property
    def has_halen_brengen(self) -> bool:
        """
        Controleer of er instrumenten gehaald en gebracht moeten worden.
        """
        return self.has_brengen() and self.has_halen()
    
    @property
    def laadtijd(self) -> Long_time:
        """
        De laadtijd van de taak.
        """
        tijd = Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT + self._halen.laadtijd + self._brengen.laadtijd
        return Long_time(tijd)
    
    @property
    def begintijd_taak(self) -> Optional[Long_time]:
        """
        De begintijd van de taak.
        """
        return self._ingeplande_tijd
    
    def set_begintijd_taak(self, geplande_tijd: Long_time):
        """
        De begintijd van de taak inplannen.
        """
        self._ingeplande_tijd = geplande_tijd

    @property
    def eindtijd_taak(self) -> Optional[Long_time]:
        """
        De eindtijd van de taak.
        """
        if self._ingeplande_tijd is None:
            return None
        return self._ingeplande_tijd + self.laadtijd

    @property
    def id(self) -> int:
        """
        Het id van de taak.
        """
        return self._id
    
    @property
    def has_ingeplande_tijd(self) -> bool:
        """
        Controleer of de taak een ingeplande tijd heeft.
        """
        return self._ingeplande_tijd is not None
    
    @property
    def returntijd(self):
        """
        Geeft het tijdvak waarin de opgehaalde instrumenten schoon terug bij het ziekenhuis moeten zijn.
        """
        return self._returntijd
