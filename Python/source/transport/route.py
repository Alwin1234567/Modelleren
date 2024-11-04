from enum import Enum, auto
from source.structures import Status, Distances, ID, Taak, Long_time
from warnings import warn
from typing import List, Tuple, TYPE_CHECKING
from datetime import time, datetime, timedelta
from source.constants import Constants

if TYPE_CHECKING:    
    from source.locations import Location, Ziekenhuis, Hub

class Route_type(Enum):
    AVOND = auto()
    OCHTEND = auto()

class Route:

    # distances will be a reference to the relevant distances object
    def __init__(self, route_type: Route_type, start: "Hub", distances: Distances, capaciteit: int) -> None:
        self._distances = distances
        if self._distances.status != Status.FINISHED: 
            raise ValueError("Distances object is not finished")
        self._route_type = route_type
        self._start = start
        self._capaciteit = capaciteit
        #self._locations: List["Ziekenhuis"] = []
        self._taken: List["Taak"] = []
        self._status = Status.PREPARING
        self._id = ID()
    
    def add_taak(self, taak: "Taak", end = True) -> None:
        """
        Voeg een taak toe aan de route.
        
        Parameters:
            taak (Taak): De taak die moet worden toegevoegd.
            end (bool): True als de meegegeven taak aan eind van de route moet worden toegevoegd, False als deze aan begin van route moet worden toegevoegd.
        
        Raises:
            ValueError: Als de route niet in de preparing status is.
            ValueError: Als de locatie niet in de distances object zit.
            Warning: Als de taak al in de route zit.
        """
        if self._status != Status.PREPARING:
            raise ValueError("Route is not in preparing state")
        if not self._distances.has_location(taak.ziekenhuis):
            raise ValueError("Location is not in distances object")
        if taak in set(self._taken):
            warn("Taak is already in route")
        if end:
            self._taken.append(taak)
        self._taken.insert(0, taak)
    
    def copy(self) -> 'Route':
        """
        Maak een kopie van de route.
        
        Returns:
            Route: Een kopie van de route.
        """
        new_route = Route(self._route_type, self._start, self._distances, self._capaciteit)
        new_route._taken = self._taken.copy()
        new_route._status = self._status
        return new_route

    def make_route(self, skip_locations: list["Location"], dag: str) -> None:
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
        
        stop = False
        while not stop:
            # routes van huidige locatie naar nog toe te voegen ziekenhuizen sorteren van goedkoop naar duur
            if self.total_distance == 0:
                toe_te_voegen_routes = self._distances.available_locations(self._start, skip_locations, current_time.time())
            else:
                toe_te_voegen_routes = self._distances.available_locations(self.locations[-1], skip_locations, current_time.time())
            
            toegevoegd = False
            for huidig_naar_nieuw in toe_te_voegen_routes:
                # van goedkoopste naar duurste, alle routes naar toe te voegen ziekenhuizen controleren tot ziekenhuis kan worden toegevoegd
                nieuw_locatie = huidig_naar_nieuw[0]
                if not isinstance(nieuw_locatie, "Ziekenhuis"):
                    warn(f'{nieuw_locatie.name} is geen ziekenhuis')
                    continue
                nieuw_ziekenhuis = nieuw_locatie
                print(nieuw_ziekenhuis, huidig_naar_nieuw[1].cost(current_time.time()), huidig_naar_nieuw[1].distance, huidig_naar_nieuw[1].time)
                # maximale tijd controleren
                if t + huidig_naar_nieuw[1].time + Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT + self._distances.get_time(nieuw_ziekenhuis, self._start) > t_max:
                    print('tijd overschreden')
                    continue # met het toevoegen van dit ziekenhuis wordt de maximale tijd overschreden -> volgende proberen
                # capaciteit controleren
                print('max, weg, eind, halen:', maximale_lading, getattr(nieuw_ziekenhuis.vraag_wegbrengen, dag), lading_eindpunt, getattr(nieuw_ziekenhuis.vraag_ophalen, dag), 
                      '  max nieuw, cap:', max(maximale_lading + getattr(nieuw_ziekenhuis.vraag_wegbrengen, dag), lading_eindpunt + getattr(nieuw_ziekenhuis.vraag_ophalen, dag)), self._capaciteit)
                if max(maximale_lading + getattr(nieuw_ziekenhuis.vraag_wegbrengen, dag), lading_eindpunt + getattr(nieuw_ziekenhuis.vraag_ophalen, dag)) > self._capaciteit:
                    print('capaciteit ergens overschreden')
                    continue # toevoegen van ziekenhuis overschrijdt ergens op de route de lading
                # tijdvak controleren
                tijdvak_toevoeg_ziekenhuis = nieuw_ziekenhuis.tijdvak # tijdvak waarin ziekenhuis beschikbaar is
                if self.route_type == Route_type.AVOND:
                    aankomst_ziekenhuis: datetime = current_time + timedelta(minutes=huidig_naar_nieuw[1].time) 
                    vertrek_ziekenhuis: datetime = aankomst_ziekenhuis + timedelta(minutes=Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT) 
                else: 
                    # ochtendroute, dus terug in de tijd
                    vertrek_ziekenhuis: datetime = current_time - timedelta(minutes=huidig_naar_nieuw[1].time) 
                    aankomst_ziekenhuis: datetime = vertrek_ziekenhuis - timedelta(minutes=Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT) 
                print('current time:', current_time.time(), ' aankomsttijd:', aankomst_ziekenhuis.time(), ' vertrektijd:', vertrek_ziekenhuis.time(), "\ntijdvakken:", tijdvak_toevoeg_ziekenhuis)
                if tijdvak_toevoeg_ziekenhuis != None and (aankomst_ziekenhuis.time() <= tijdvak_toevoeg_ziekenhuis[0] or vertrek_ziekenhuis.time() >= tijdvak_toevoeg_ziekenhuis[1]):
                    print('tijdvak overschreden')
                    continue # ziekenhuis wordt bezocht buiten het toegezegde tijdvak

                # aan alle controles is voldaan, dus ziekenhuis wordt toegevoegd aan route
                print('alle controles voldoen. Ziekenhuis toevoegen aan route\n')
                toegevoegd = True
                skip_locations.append(nieuw_ziekenhuis)
                self.add_location(nieuw_ziekenhuis)
                # tijden updaten
                reistijd_wachttijd: float = huidig_naar_nieuw[1].time + Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT # in minuten
                t += reistijd_wachttijd 
                if self.route_type == Route_type.AVOND:
                    current_time = current_time + timedelta(minutes=reistijd_wachttijd) 
                else:
                    current_time = current_time - timedelta(minutes=reistijd_wachttijd) 
                # lading updaten
                maximale_lading = max(maximale_lading + getattr(nieuw_ziekenhuis.vraag_wegbrengen, dag), lading_eindpunt + getattr(nieuw_ziekenhuis.vraag_ophalen, dag))
                lading_startpunt += getattr(nieuw_ziekenhuis.vraag_wegbrengen, dag)
                lading_eindpunt += getattr(nieuw_ziekenhuis.vraag_ophalen, dag)
                break # nieuwe routes berekenen vanaf toegevoegde ziekenhuis

            if toegevoegd == False:
                print('alle ziekenhuizen bekeken, geen kon worden toegevoegd')
                # geen van de ziekenhuizen kon worden toegevoegd
                stop = True 
        if self.route_type == Route_type.OCHTEND:
            # route moet worden omgedraaid, omdat hij in omgekeerde volgorde wordt gereden dan hij is gemaakt
            self._locations.reverse()

        return toe_te_voegen_routes
    
    def maak_route_2(self, starttaak: Taak, taken) -> None:
        """
        Maak een startoplossing voor de route.
        Vult self._taken met ziekenhuizen in de volgorde waarop ze in de route voorkomen.

        Parameters:
            starttaak (Taak): De taak die in deze route moet zitten, van waaruit de route wordt opgebouwd.
            taken: Alle taken die nog niet in een route zitten.
        """
        if self._status == Status.FINISHED:
            raise ValueError("Route is not in preparing state")
        pass

    @property
    def start_tijd(self) -> Long_time:
        if not self._taken:
            return None
        reistijd_vanaf_hub = self._distances.get_time(self._start, self._taken[0].ziekenhuis)
        start_tijd = self._taken[0].begintijd_taak - reistijd_vanaf_hub
        return start_tijd
    
    @property
    def eind_tijd(self) -> Long_time:
        if not self._taken:
            return None
        reistijd_naar_hub = self._distances.get_time(self._taken[-1].ziekenhuis, self._start)
        eind_tijd = self._taken[-1].eindtijd_taak + reistijd_naar_hub
        return eind_tijd

    @property
    def status(self) -> Status:
        return self._status
    
    @property
    def taken(self) -> List["Taak"]:
        return self._taken
    
    @property
    def route_type(self) -> Route_type:
        return self._route_type
    
    @property
    def start(self) -> "Hub":
        return self._start
    
    @property
    def total_distance(self) -> float:
        """
        Bereken de totale afstand van de route.
        
        Returns:
            float: De totale afstand van de route.
        """
        if not self._taken:
            return 0
        
        total_distance = 0
        total_distance += self._distances.get_distance(self._start, self._taken[0].ziekenhuis)
        for i in range(len(self._taken) - 1):
            total_distance += self._distances.get_distance(self._taken[i].ziekenhuis, self._taken[i + 1].ziekenhuis)
        total_distance += self._distances.get_distance(self._taken[-1].ziekenhuis, self._start)
        return total_distance

    @property
    def total_time(self) -> float:
        """
        Bereken de totale tijd van de route.
        
        Returns:
            float: De totale tijd van de route.
        """
        if not self._taken:
            return 0
        
        total_time = self.eind_tijd - self.start_tijd
        if total_time < 0:
            ValueError('De route eindigd op een eerder tijdstip dan deze begint')
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
        if not self._taken:
            return 0
        
        total_cost = 0
        total_cost += self._distances.get_distance_time(self._start, self._taken[0].ziekenhuis).cost(self.start_tijd)
        
        for i in range(len(self._taken) - 1):
            total_cost += self._taken[i].cost_with_taak(self._taken[i + 1], self._distances, end = True)
        total_cost += self._distances.get_distance_time(self._taken[-1].ziekenhuis, self._start).cost(self._taken[-1].eindtijd_taak)
        return total_cost

    @property   
    def departure_times(self) -> List[Tuple["Ziekenhuis", time]]:
        """
        Bepaal de vertrektijden bij elk ziekenhuis

        Returns:
            List[Tuple[Ziekenhuis, time]]: de vertrektijden bij de ziekenhuizen in de route
        """
        if not self._taken:
            return []
        
        departure_times = []
        for i in range(len(self._taken)):
            departure_times.append(self._taken[i].eindtijd_taak)

        return departure_times
