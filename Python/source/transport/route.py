from enum import Enum, auto
from source.locations import Location, Ziekenhuis, Hub
from source.structures import Status, Distances, ID
from warnings import warn
from typing import List
import datetime
from datetime import time
from source.constants import Constants

class Route_type(Enum):
    AVOND = auto()
    OCHTEND = auto()

class Route:

    # destances will be a reference to the relevant distances object
    def __init__(self, route_type: Route_type, start: Hub, distances: Distances) -> None:
        self._distances = distances
        #if self._distances.status != Status.FINISHED: # controle tijdelijk weg voor testen zonder dat maps nodig is
            #raise ValueError("Distances object is not finished")
        self._route_type = route_type
        self._start = start
        self._locations: List[Ziekenhuis] = []
        self._status = Status.PREPARING
        self._id = ID()
    
    def add_location(self, location: Ziekenhuis) -> None:
        """
        Voeg een ziekenhuis toe aan de route.
        
        Parameters:
            location (Ziekenhuis): Het ziekenhuis dat moet worden toegevoegd.
        
        Raises:
            ValueError: Als de route niet in de preparing status is.
            ValueError: Als de locatie niet in de distances object zit.
            Warning: Als de locatie al in de route zit.
        """
        if self._status != Status.PREPARING:
            raise ValueError("Route is not in preparing state")
        if not self._distances.has_location(location):
            raise ValueError("Location is not in distances object")
        if location in set(self._locations):
            warn("Location is already in route")
        self._locations.append(location)
    
    def copy(self) -> 'Route':
        """
        Maak een kopie van de route.
        
        Returns:
            Route: Een kopie van de route.
        """
        new_route = Route(self._route_type, self._start, self._distances)
        new_route._locations = self._locations.copy()
        new_route._status = self._status
        return new_route
    
    def make_route(self, toe_te_voegen_ziekenhuizen: List[Ziekenhuis]) -> None:
        """
        Maak een startoplossing voor de route.
        Vult self._locations met ziekenhuizen in de volgorde waarop ze in de route voorkomen.

        Parameters:
            toe_te_voegen_ziekenhuizen (List[Location]): lijst met ziekenhuizen die nog niet in een route zitten
        """
        capaciteit: float = 10  # voor nu capaciteit hierin, maar moet aan object worden meegegeven vanuit auto
        t_max: float = 14*60   # aantal minuten die de route maximaal mag duren
        t = 0   # tijdsduur huidige route (self.total_time?)
        current_time: datetime = datetime.datetime(1900,1,1, self.start_tijd.hour, self.start_tijd.minute, self.start_tijd.second) # huidige tijd in de route
        vertreklading_huidige_punt: float = 0
        lading_startpunt: float = 0
        al_geprobeerde_ziekenhuizen: List[Ziekenhuis] = []

        i = -1 #testvariabele

        while t < t_max and len(toe_te_voegen_ziekenhuizen) > 0 and i < (len(toe_te_voegen_ziekenhuizen)-1):
            print('while start', len(toe_te_voegen_ziekenhuizen), i)
            i += 1
            # controleer of er nog tijd is om naar een ander ziekenhuis te gaan
            distance_closest_ziekenhuis = 10 # minimale afstand naar nieuw ziekenhuis vanaf huidige ziekenhuis 
            distance_closest_ziekenhuis_to_hub = 12 # afstand van nieuwe ziekenhuis in bovenstaande variabele naar hub
            distance_closest_to_hub = 9 # minimale afstand van nieuw ziekenhuis naar hub
            distance_closest_to_hub_to_ziekenhuis = 12 # afstand van huidige ziekenhuis naar nieuwe ziekenhuis in bovenstaande variabele
            if t + distance_closest_ziekenhuis + Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT + distance_closest_ziekenhuis_to_hub > t_max:
                print('break1')
                break # met het toevoegen van het dichtsbijzijnde ziekenhuis wordt de maximale tijd overschreden
            if t + distance_closest_to_hub_to_ziekenhuis + Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT + distance_closest_to_hub > t_max:
                print('break2')
                break # met het toevoegen van het ziekenhuis dat het dichts bij de hub ligt wordt de maximale tijd overschreden
            print('nog tijd voor extra ziekenhuis')
            toevoeg_ziekenhuis = toe_te_voegen_ziekenhuizen[i] # moet dichtsbijzijndste ziekenhuis worden
            
            # constraints controleren
            reistijd_toevoeg_ziekenhuis = 10 # reistijd naar het nieuwe ziekenhuis
            reistijd_toevoeg_ziekenhuis_to_hub = 10 # reistijd van nieuwe ziekenhuis naar hub
            brenghoeveelheid_toevoeg_ziekenhuis = 10 # hoveelheid instrumentensets die afgeleverd moeten worden
            ophaalhoeveelheid_toevoeg_ziekenhuis = 10 # hoeveelheid instrumentensets die opgehaald moet worden
            tijdvak_toevoeg_ziekenhuis = (time(6, 0), time(20, 0)) # tijdvak waarin ziekenhuis beschikbaar is
            if t + reistijd_toevoeg_ziekenhuis + reistijd_toevoeg_ziekenhuis_to_hub + Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT > t_max:
                print('continue1')
                # toevoegen van ziekenhuis overschrijdt de maximale tijdsduur van de route
                continue
            print(lading_startpunt, brenghoeveelheid_toevoeg_ziekenhuis, capaciteit)
            if lading_startpunt + brenghoeveelheid_toevoeg_ziekenhuis > capaciteit:
                print('continue2 ', i)
                # toevoegen van ziekenhuis overschrijdt de capaciteit van het voertuig op het beginpunt
                continue
            print(vertreklading_huidige_punt, brenghoeveelheid_toevoeg_ziekenhuis, ophaalhoeveelheid_toevoeg_ziekenhuis, capaciteit)
            if vertreklading_huidige_punt - brenghoeveelheid_toevoeg_ziekenhuis + ophaalhoeveelheid_toevoeg_ziekenhuis > capaciteit:
                print('continue3')
                # toevoegen van ziekenhuis overschrijdt de capaciteit van het voertuig bij het vertrekken vanaf dit ziekenhuis
                continue
            print(tijdvak_toevoeg_ziekenhuis, tijdvak_toevoeg_ziekenhuis[0], tijdvak_toevoeg_ziekenhuis[1], current_time.time())
            if tijdvak_toevoeg_ziekenhuis != None and current_time.time() < tijdvak_toevoeg_ziekenhuis[0] and current_time.time() > tijdvak_toevoeg_ziekenhuis[1]:
                print('continue4')
                # ziekenhuis wordt bezocht buiten het toegezegde tijdvak
                continue
            print('constraints voldaan ', i)
            # constraints zijn voldaan
            self.add_location(toevoeg_ziekenhuis)
            print('actie')
            reistijd_wachttijd = reistijd_toevoeg_ziekenhuis + Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT # in minuten
            print('actie')
            t += reistijd_wachttijd # (self.total_time?)
            print('actie')
            current_time = current_time + datetime.timedelta(minutes=reistijd_wachttijd) 
            print('actie')
            lading_startpunt += brenghoeveelheid_toevoeg_ziekenhuis
            print('actie')
            vertreklading_huidige_punt += (ophaalhoeveelheid_toevoeg_ziekenhuis - brenghoeveelheid_toevoeg_ziekenhuis)
            # toevoeg_ziekenhuis verwijderen uit toe_te_voegen_ziekenhuizen
            toe_te_voegen_ziekenhuizen.remove(toevoeg_ziekenhuis)
            print(len(toe_te_voegen_ziekenhuizen))
            print('eind loop ', i)

        print('klaar, niks kan meer worden toegevoegd')


    @property
    def start_tijd(self) -> time:
        if self._route_type == Route_type.AVOND:
            return time(17, 0)
        else:
            # dit is eindtijd voor ochtendroute, wat is de starttijd?
            return time(7, 0)
    
    @property
    def status(self) -> Status:
        return self._status
    
    @property
    def locations(self) -> List[Ziekenhuis]:
        return self._locations
    
    @property
    def route_type(self) -> Route_type:
        return self._route_type
    
    @property
    def start(self) -> Hub:
        return self._start
    
    @property
    def total_distance(self) -> float:
        """
        Bereken de totale afstand van de route.
        
        Returns:
            float: De totale afstand van de route.
        """
        total_distance = 0
        total_distance += self._distances.get_distance(self._start, self._locations[0])
        for i in range(len(self._locations) - 1):
            total_distance += self._distances.get_distance(self._locations[i], self._locations[i + 1])
        total_distance += self._distances.get_distance(self._locations[-1], self._start)
        return total_distance

    @property
    def total_time(self) -> float:
        """
        Bereken de totale tijd van de route.
        
        Returns:
            float: De totale tijd van de route.
        """
        total_time = 0
        total_time += self._distances.get_time(self._start, self._locations[0])
        for i in range(len(self._locations) - 1):
            total_time += self._distances.get_time(self._locations[i], self._locations[i + 1])
        total_time += self._distances.get_time(self._locations[-1], self._start)
        return total_time

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def cost(self) -> float:
        """
        Bereken de kosten van de route.
        
        Returns:
            float: De kosten van de route.
        """
        return 0.0
