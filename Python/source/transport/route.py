from enum import Enum, auto
from source.locations import Location, Ziekenhuis, Hub
from source.structures import Status, Distances, ID
from warnings import warn
from typing import List, Tuple
from datetime import time, datetime, timedelta
from source.constants import Constants

class Route_type(Enum):
    AVOND = auto()
    OCHTEND = auto()

class Route:

    # destances will be a reference to the relevant distances object
    def __init__(self, route_type: Route_type, start: Hub, distances: Distances, capaciteit: int) -> None:
        self._distances = distances
        if self._distances.status != Status.FINISHED: 
            raise ValueError("Distances object is not finished")
        self._route_type = route_type
        self._start = start
        self._capaciteit = capaciteit
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

    def make_route(self, skip_locations: list["Location"]) -> None:
        """
        Maak een startoplossing voor de route.
        Vult self._locations met ziekenhuizen in de volgorde waarop ze in de route voorkomen.

        Parameters:
            skip_locations (List[Location]): lijst met locaties die al in een route zitten
        """
        t_max: float = 14*60   # aantal minuten die de route maximaal mag duren
        t: float = 0   # tijdsduur huidige route in minuten
        current_time: datetime = datetime(1900,1,1, self.start_tijd.hour, self.start_tijd.minute, self.start_tijd.second) # huidige tijd in de route
        lading_startpunt: float = 0
        lading_eindpunt: float = 0
        maximale_lading: float = 0

        skip_locations.append(self._start)
        
        stop: bool = False
        while stop == False:
            # routes van huidige locatie naar nog toe te voegen ziekenhuizen sorteren van goedkoop naar duur
            if self.total_distance == 0:
                toe_te_voegen_routes = self._distances.available_locations(self._start, skip_locations, current_time.time())
            else:
                toe_te_voegen_routes = self._distances.available_locations(self.locations[-1], skip_locations, current_time.time())
            
            toegevoegd: bool = False
            for huidig_naar_nieuw in toe_te_voegen_routes:
                # van goedkoopste naar duurste, alle routes naar toe te voegen ziekenhuizen controleren tot ziekenhuis kan worden toegevoegd
                nieuw_ziekenhuis: Ziekenhuis = huidig_naar_nieuw[0]
                print(nieuw_ziekenhuis, huidig_naar_nieuw[1].cost(current_time.time()), huidig_naar_nieuw[1].distance, huidig_naar_nieuw[1].time)
                # maximale tijd controleren
                if t + huidig_naar_nieuw[1].time + Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT + self._distances.get_time(nieuw_ziekenhuis, self._start) > t_max:
                    print('tijd overschreden')
                    continue # met het toevoegen van dit ziekenhuis wordt de maximale tijd overschreden -> volgende proberen
                # capaciteit controleren
                print('max, weg, eind, halen: ', maximale_lading, nieuw_ziekenhuis.vraag_wegbrengen.monday, lading_eindpunt, nieuw_ziekenhuis.vraag_ophalen.monday)
                print('max nieuw, cap: ', max(maximale_lading + nieuw_ziekenhuis.vraag_wegbrengen.monday, lading_eindpunt + nieuw_ziekenhuis.vraag_ophalen.monday), self._capaciteit)
                if max(maximale_lading + nieuw_ziekenhuis.vraag_wegbrengen.monday, lading_eindpunt + nieuw_ziekenhuis.vraag_ophalen.monday) > self._capaciteit:
                    print('capaciteit ergens overschreden')
                    continue # toevoegen van ziekenhuis overschrijdt ergens op de route de lading
                # tijdvak controleren
                tijdvak_toevoeg_ziekenhuis = nieuw_ziekenhuis.tijdvak # tijdvak waarin ziekenhuis beschikbaar is
                aankomst_ziekenhuis = current_time + timedelta(minutes=huidig_naar_nieuw[1].time) 
                vertrek_ziekenhuis = aankomst_ziekenhuis + timedelta(minutes=Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT) 
                print('current time = ', current_time, 'aankomsttijd = ', aankomst_ziekenhuis, 'vertrektijd = ', vertrek_ziekenhuis, "tijdvakken:", tijdvak_toevoeg_ziekenhuis)
                if tijdvak_toevoeg_ziekenhuis != None and (aankomst_ziekenhuis.time() <= tijdvak_toevoeg_ziekenhuis[0] or vertrek_ziekenhuis.time() >= tijdvak_toevoeg_ziekenhuis[1]):
                    print('tijdvak overschreden')
                    continue # ziekenhuis wordt bezocht buiten het toegezegde tijdvak

                # aan alle controles is voldaan, dus ziekenhuis wordt toegevoegd aan route
                print('alle controles voldoen. Ziekenhuis toevoegen aan route')
                toegevoegd = True
                skip_locations.append(nieuw_ziekenhuis)
                self.add_location(nieuw_ziekenhuis)
                # tijden updaten
                reistijd_wachttijd = huidig_naar_nieuw[1].time + Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT # in minuten
                t += reistijd_wachttijd 
                current_time = current_time + timedelta(minutes=reistijd_wachttijd) 
                # lading updaten
                maximale_lading = max(maximale_lading + nieuw_ziekenhuis.vraag_wegbrengen.monday, lading_eindpunt + nieuw_ziekenhuis.vraag_ophalen.monday)
                lading_startpunt += nieuw_ziekenhuis.vraag_wegbrengen.monday
                lading_eindpunt += nieuw_ziekenhuis.vraag_ophalen.monday

                # controlestukje
                for huidig_naar_nieuw in toe_te_voegen_routes:
                    print(huidig_naar_nieuw[0], huidig_naar_nieuw[1].cost(current_time.time()), huidig_naar_nieuw[1].distance, huidig_naar_nieuw[1].time)
                break

            if toegevoegd == False:
                print('alle ziekenhuizen bekeken, geen kon worden toegevoegd')
                # geen van de ziekenhuizen kan worden toegevoegd
                stop = True 
        return toe_te_voegen_routes
 
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
        if self._locations != []:
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
        if self._locations != []:
            total_time += self._distances.get_time(self._start, self._locations[0])
            for i in range(len(self._locations) - 1):
                total_time += self._distances.get_time(self._locations[i], self._locations[i + 1])
            total_time += self._distances.get_time(self._locations[-1], self._start)
        return total_time

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def total_cost(self) -> float:
        """
        Bereken de kosten van de route.
        
        Returns:
            float: De kosten van de route.
        """
        total_cost = 0
        if self._locations != []:
            total_cost += self._distances.get_distance_time(self._start, self._locations[0]).cost(self.start_tijd)
            for i in range(len(self._locations) - 1):
                total_cost += self._distances.get_distance_time(self._locations[i], self._locations[i + 1]).cost(self.departure_times[i][1])
            total_cost += self._distances.get_distance_time(self._locations[-1], self._start).cost(self.departure_times[-1][1])
        return total_cost
        
    @property
    def departure_times(self) -> List[Tuple[Ziekenhuis, time]]:
        """
        Bepaal de vertrektijden bij elk ziekenhuis

        Returns:
            List[Tuple[Ziekenhuis, time]]: de vertrektijden bij de ziekenhuizen in de route
        """
        departure_times = []
        current_time: datetime = datetime(1900,1,1, self.start_tijd.hour, self.start_tijd.minute, self.start_tijd.second) # huidige tijd in de route
        if self._locations != []:
            travel_wait_time = self._distances.get_time(self._start, self._locations[0]) + Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT
            current_time = current_time + timedelta(minutes=travel_wait_time)
            departure_times.append((self._locations[0], current_time.time()))
            for i in range(len(self._locations) - 1):
                travel_wait_time = self._distances.get_time(self._locations[i], self._locations[i + 1]) + Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT
                current_time = current_time + timedelta(minutes=travel_wait_time)
                departure_times.append((self._locations[i+1], current_time.time()))
        return departure_times
