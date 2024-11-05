from enum import Enum, auto
from source.structures import Status, Distances, ID, Taak, Long_time, Cost
from warnings import warn
from typing import List, Tuple, TYPE_CHECKING, Optional
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
        else:
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
    
    def maak_route_2(self, starttaak: Taak, nog_te_plannen_taken: list[Taak]) -> None:
        """
        Maak een startoplossing voor de route.
        Vult self._taken met ziekenhuizen in de volgorde waarop ze in de route voorkomen.

        Parameters:
            starttaak (Taak): De taak die in deze route moet zitten, van waaruit de route wordt opgebouwd.
            nog_te_plannen_taken (list[Taak]): Alle taken die nog niet in een route zitten.
        """
        if self._status == Status.FINISHED:
            raise ValueError("Route is not in preparing state")
        
        self.add_taak(starttaak)
        starttaak.set_begintijd_taak(starttaak.tijdslot.starttijd) # starttijd van toegestane tijdslot nemen als begintijd van de taak
        startlading = starttaak.brengen
        eindlading = starttaak.halen
        max_lading = max(startlading, eindlading)
        if starttaak.returntijd == None:
            t_max = Long_time(7*24*60) # eindtijd van gehele planning
        else: 
            t_max = starttaak.returntijd.eindtijd - Constants.TIJDSDUUR_SCHOONMAAK - self._distances.get_time(self.start, starttaak.ziekenhuis)
        
        for _ in range(len(nog_te_plannen_taken)):
            max_wegbrengen = self._capaciteit - max_lading
            max_ophalen = self._capaciteit - eindlading
            vooraan_taak, vooraan_max_starttijd = self.vooraan_toe_te_voegen(nog_te_plannen_taken, self._taken[0], self._taken[-1], max_wegbrengen, max_ophalen)
            achteraan_taak, achteraan_starttijd = self.achteraan_toe_te_voegen(nog_te_plannen_taken, self._taken[-1], max_wegbrengen, max_ophalen, t_max)
            toevoeg_taken = []
            
            if vooraan_taak == None and achteraan_taak == None:
                print('geen taken meer toe te voegen')
                # stoppen met route maken
                break
            
            if vooraan_taak != None:
                max_eindtijd = vooraan_max_starttijd + vooraan_taak.laadtijd
                if max_eindtijd > vooraan_taak.tijdslot.eindtijd:
                    # tijdvak eindigd voor maximale eindttijd, dus eindtijd tijdslot wordt eindtijd
                    starttijd = vooraan_taak.tijdslot.eindtijd - vooraan_taak.laadtijd
                else:
                    starttijd = vooraan_max_starttijd
                kosten = self._taken[0].cost_with_taak(vooraan_taak, self._distances, False)
                toevoeg_taken.append([vooraan_taak, False, starttijd, kosten])
                print('vooraan', vooraan_taak.ziekenhuis, vooraan_taak.brengen, 'kosten:', kosten)
            if achteraan_taak != None:
                kosten = self._taken[-1].cost_with_taak(achteraan_taak, self._distances, True)
                toevoeg_taken.append([achteraan_taak, True, achteraan_starttijd, kosten])
                print('achteraan', achteraan_taak.ziekenhuis, achteraan_taak.brengen, 'kosten:', kosten)

            if len(toevoeg_taken) == 2:
                # taken sorteren op kosten
                toevoeg_taken.sort(key = lambda taak: taak[-1])
            
            # taak met laagste kosten (of enige taak) toevoegen
            taak = toevoeg_taken[0][0]
            if not isinstance(taak, Taak):
                warn(f'{taak} is geen taak')
            
            self.add_taak(taak, toevoeg_taken[0][1])
            taak.set_begintijd_taak(toevoeg_taken[0][2])
            startlading += taak.brengen
            eindlading += taak.halen
            max_lading = max(max_lading + taak.brengen, eindlading)
            if taak.returntijd != None and taak.returntijd.starttijd < t_max:
                t_max = taak.returntijd.eindtijd - Constants.TIJDSDUUR_SCHOONMAAK - self._distances.get_time(self.start, taak.ziekenhuis)
            
            # taak weghalen uit taken
            nog_te_plannen_taken.remove(taak)
        
        self._status = Status.FINISHED

    def vooraan_toe_te_voegen(self, nog_te_plannen_taken: list[Taak], eerste_taak: Taak, laatste_taak: Taak, max_wegbrengen: int, max_ophalen: int) -> Optional[Tuple[Taak, Long_time]]:
        """
        Geeft de goedkoopste taak die vooraan aan de route kan worden toegevoegd.
        
        Parameters:
            nog_te_plannen_taken (list[Taak]): Lijst met taken die nog in een route moeten komen.
            eerste_taak (Taak): Eerste taak in de route.
            laatste_taak (Taak): Laatste taak in de route.
            max_wegbrengen (int): Maximale hoeveelheid die bij het ziekenhuis afgeleverd kan worden.
            max_ophalen (int): Maximale hoeveelheid die bij het ziekenhuis opgehaald kan worden.
        
        Returns:
            Optional[list[Taak, Long_time]]: Taak die voor de route kan worden toegevoegd met de bijbehorende maximale starttijd of None als er geen taak voor kan worden toegevoegd.
        """
        # alleen taken voor eerste_taak en met toegestane hoeveelheid brengen en ophalen
        # gefilterd = list(filter(lambda taak: taak.tijdslot.starttijd < eerste_taak.begintijd_taak and taak.brengen <= max_wegbrengen and taak.halen <= max_ophalen, nog_te_plannen_taken))
        
        gefilterd = [taak for taak in nog_te_plannen_taken if taak.tijdslot.starttijd < eerste_taak.begintijd_taak and taak.brengen <= max_wegbrengen and taak.halen <= max_ophalen]
    
        # sorteren op kosten van toevoegen taak voor eerste_taak
        gefilterd.sort(key = lambda taak: eerste_taak.cost_with_taak(taak, self._distances, False))
        
        tijd_terug_hub = laatste_taak.eindtijd_taak + self._distances.get_time(laatste_taak.ziekenhuis, self._start)
        for taak in gefilterd:
            reistijd = self._distances.get_time(taak.ziekenhuis, eerste_taak.ziekenhuis)
            max_starttijd = eerste_taak.begintijd_taak - reistijd - taak.laadtijd
            if taak.tijdslot.starttijd > max_starttijd:
                # starttijd van taak moet voor maximale tijdslot liggen
                continue # volgende taak bekijken
            if taak.returntijd.eindtijd - Constants.TIJDSDUUR_SCHOONMAAK - self._distances.get_time(self.start, taak.ziekenhuis) < tijd_terug_hub:
                # route moet optijd terug zijn om genoeg tijd te geven voor schoonmaak
                continue # volgende taak bekijken
            # taak voldoet aan alle criteria
            taak_vooraan = taak
            return taak_vooraan, max_starttijd
        return None

    def achteraan_toe_te_voegen(self, nog_te_plannen_taken: list[Taak], laatste_taak: Taak, max_wegbrengen: int, max_ophalen: int, t_max: Long_time) -> Optional[Tuple[Taak, Long_time]]:
        """
        Geeft de goedkoopste taak die achteraan aan de route kan worden toegevoegd.
        
        Parameters:
            nog_te_plannen_taken (list[Taak]): Lijst met taken die nog in een route moeten komen.
            laatste_taak (Taak): Laatste taak in de route.
            max_wegbrengen (int): Maximale hoeveelheid die bij het ziekenhuis afgeleverd kan worden.
            max_ophalen (int): Maximale hoeveelheid die bij het ziekenhuis opgehaald kan worden.
            t_max (Long_time): De uiterlijke tijd waarop er bij een ziekenhuis moet worden vertrokken om op tijd terug te zijn om de al opgehaalde instrumenten op tijd schoon te maken. 
        
        Returns:
            Optional[list[Taak, Long_time]]: Taak die voor de route kan worden toegevoegd met de bijbehorende maximale starttijd of None als er geen taak voor kan worden toegevoegd.
        """
        # alleen taken voor eerste_taak en met toegestane hoeveelheid brengen en ophalen
        # gefilterd = list(filter(lambda taak: taak.tijdslot.starttijd > laatste_taak.eindtijd_taak and taak.brengen <= max_wegbrengen and taak.halen <= max_ophalen, nog_te_plannen_taken))

        gefilterd = [taak for taak in nog_te_plannen_taken if taak.tijdslot.starttijd > laatste_taak.eindtijd_taak and taak.brengen <= max_wegbrengen and taak.halen <= max_ophalen]
        
        # sorteren op kosten van toevoegen taak voor eerste_taak
        gefilterd.sort(key = lambda taak: laatste_taak.cost_with_taak(taak, self._distances, True))
        
        for taak in gefilterd:
            reistijd = self._distances.get_time(laatste_taak.ziekenhuis, taak.ziekenhuis)
            min_eindtijd = laatste_taak.eindtijd_taak + reistijd + taak.laadtijd
            starttijd = laatste_taak.eindtijd_taak + reistijd
            if taak.tijdslot.eindtijd < min_eindtijd:
                # eindtijd van taak moet na maximale tijdslot liggen
                continue # volgende taak bekijken
            reistijd_terug_hub = self._distances.get_time(taak.ziekenhuis, self._start)
            if taak.returntijd.eindtijd - Constants.TIJDSDUUR_SCHOONMAAK - self._distances.get_time(self.start, taak.ziekenhuis) < min_eindtijd + reistijd_terug_hub:
                # route moet optijd terug zijn om genoeg tijd te geven voor schoonmaak
                continue # volgende taak bekijken
            if taak.tijdslot.starttijd > min_eindtijd - taak.laadtijd:
                # start tijdslot ligt na minimale starttijd -> starttijd wordt start tijdslot
                starttijd = taak.tijdslot.starttijd
                tijd_terug_hub = taak.tijdslot.starttijd + taak.laadtijd + reistijd_terug_hub 
                if taak.returntijd.eindtijd - Constants.TIJDSDUUR_SCHOONMAAK - self._distances.get_time(self.start, taak.ziekenhuis) < tijd_terug_hub:
                    # route moet optijd tuerg izjn om genoeg tijd te geven voor schoonmaak
                    continue
            if starttijd + taak.laadtijd > t_max:
                # toevoegen zorgt dat instrumenten van route niet op tijd terug zijn om schoongemaakt te worden
                continue
            # taak voldoet aan alle criteria
            return taak, starttijd
        return None

    @property
    def start_tijd(self) -> Optional[Long_time]:
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
        
        total_time = self.eind_tijd - self.start_tijd # zorgt voor waarschuwing bij negatieve waarde
        if total_time < 0:
            raise ValueError('De route eindigd op een eerder tijdstip dan deze begint')
        
        total_time = self.eind_tijd.difference(self.start_tijd)
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
        
        distance_cost = Cost.calculate_cost_distance(self.total_distance)
        time_cost = Cost.calculate_cost_time(self.start_tijd.tijd, self.total_time)
        
        return distance_cost + time_cost

    @property   
    def departure_times(self) -> List[Tuple["Taak", Long_time]]:
        """
        Bepaal de vertrektijden bij het ziekenhuis van elke taak

        Returns:
            List[Tuple[Taak, Long_time]]: de vertrektijden bij de ziekenhuizen van de taken in de route
        """
        if not self._taken:
            return []
        
        departure_times = []
        for i in range(len(self._taken)):
            departure_times.append([self._taken[i], self._taken[i].eindtijd_taak])

        return departure_times
