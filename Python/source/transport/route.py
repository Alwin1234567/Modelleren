from source.structures import Status, Distances, ID, Taak, Long_time, Cost, Tijdslot, Auto_type, Bak_kar_voorkeur
from warnings import warn
from typing import List, Tuple, TYPE_CHECKING, Optional
from source.constants import Constants
from source.constants import Constants

if TYPE_CHECKING:    
    from source.locations import Hub

class Route:

    # distances will be a reference to the relevant distances object
    def __init__(self, start_hub: "Hub", distances: Distances, auto_type: Auto_type = Auto_type.BAKWAGEN) -> None:
        self._distances = distances
        if self._distances.status != Status.FINISHED: 
            raise ValueError("Distances object is not finished")
        self._start_hub = start_hub
        self._auto_type = auto_type
        self._capaciteit = Constants.capaciteit_auto(self._auto_type)
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
            ValueError: Als een taak een kar-voorkeur heeft en de route in een bestelbus zit
            Warning: Als de taak al in de route zit.
        """
        if self._status != Status.PREPARING:
            # raise ValueError("Route is not in preparing state")
            warn("Route is not in preparing state", RuntimeWarning)
        if not self._distances.has_location(taak.ziekenhuis):
            raise ValueError("Location is not in distances object")
        if self._auto_type == Auto_type.BESTELBUS and taak.ziekenhuis.voorkeur_bak_kar == Bak_kar_voorkeur.KAR:
            raise ValueError("Een taak met kar-voorkeur kan niet in een route van een bestelbus")
        if taak in self._taken:
            warn("Taak is already in route")
        if end:
            self._taken.append(taak)
        else:
            self._taken.insert(0, taak)
    
    def remove_taak(self, taak: "Taak") -> None:
        """
        Verwijder een taak uit de route.
        
        Parameters:
            taak (Taak): De taak die moet worden toegevoegd.
        
        Raises:
            ValueError: Als de route niet in de finished status is.
            ValueError: Als de locatie niet in de distances object zit.
            Warning: Als de taak al in de route zit.
        """
        if self._status != Status.FINISHED:
            raise ValueError("Route is not in preparing state")
        if taak not in self._taken:
            warn("Taak is not in route")
        self._taken.remove(taak)
    
    def copy(self) -> 'Route':
        """
        Maak een kopie van de route.
        
        Returns:
            Route: Een kopie van de route.
        """
        new_route = Route(self._start_hub, self._distances, self._auto_type)
        new_route._taken = self._taken.copy()
        new_route._status = self._status
        return new_route
    
    def maak_route(self, starttaak: Taak, nog_te_plannen_taken: list[Taak]) -> None:
        """
        Maak een startoplossing voor de route.
        Vult self._taken met ziekenhuizen in de volgorde waarop ze in de route voorkomen.

        Parameters:
            starttaak (Taak): De taak die in deze route moet zitten, van waaruit de route wordt opgebouwd.
            nog_te_plannen_taken (list[Taak]): Alle taken die nog niet in een route zitten (ook zonder de starttaak).
        """
        if self._status == Status.FINISHED:
            raise ValueError("Route is not in preparing state")
        
        self.add_taak(starttaak)
        starttaak.set_begintijd_taak(starttaak.tijdslot.starttijd) # starttijd van toegestane tijdslot nemen als begintijd van de taak
        startlading = starttaak.brengen.aantal(self._auto_type)
        eindlading = starttaak.halen.aantal(self._auto_type)
        max_lading = max(startlading, eindlading)
        t_max = starttaak.returntijd.eindtijd - Constants.TIJDSDUUR_SCHOONMAAK - self._distances.get_time(self._start_hub, starttaak.ziekenhuis)
        starttijd_route = self.start_tijd
        
        for _ in range(len(nog_te_plannen_taken)):
            max_wegbrengen = self._capaciteit - max_lading
            max_ophalen = self._capaciteit - eindlading
            vooraan_taak, vooraan_starttijd, t_max_taak_voor = self.vooraan_toe_te_voegen(nog_te_plannen_taken, self._taken[0], self._taken[-1], max_wegbrengen, max_ophalen)
            achteraan_taak, achteraan_starttijd, t_max_taak_achter = self.achteraan_toe_te_voegen(nog_te_plannen_taken, self._taken[-1], max_wegbrengen, max_ophalen, t_max, starttijd_route)
            toevoeg_taken = []
            
            if vooraan_taak == None and achteraan_taak == None:
                # stoppen met route maken
                break
            
            if vooraan_taak != None:
                # max_eindtijd = vooraan_max_starttijd + vooraan_taak.laadtijd
                # if max_eindtijd > vooraan_taak.tijdslot.eindtijd:
                #     # tijdvak eindigd voor maximale eindttijd, dus eindtijd tijdslot wordt eindtijd
                #     starttijd = vooraan_taak.tijdslot.eindtijd - vooraan_taak.laadtijd
                # else:
                #     starttijd = vooraan_max_starttijd
                kosten = self._taken[0].cost_with_taak(vooraan_taak, self._distances, self._auto_type, False)
                toevoeg_taken.append([vooraan_taak, False, vooraan_starttijd, t_max_taak_voor, kosten])
            if achteraan_taak != None:
                kosten = self._taken[-1].cost_with_taak(achteraan_taak, self._distances, self._auto_type, True)
                toevoeg_taken.append([achteraan_taak, True, achteraan_starttijd, t_max_taak_achter, kosten])

            # taken sorteren op kosten
            toevoeg_taken.sort(key = lambda taak: taak[-1])
            
            # taak met laagste kosten (of enige taak) toevoegen
            taak = toevoeg_taken[0][0]
            if not isinstance(taak, Taak):
                warn(f'{taak} is geen taak')
            
            self.add_taak(taak, toevoeg_taken[0][1])
            taak.set_begintijd_taak(toevoeg_taken[0][2])
            startlading += taak.brengen.aantal(self._auto_type)
            eindlading += taak.halen.aantal(self._auto_type)
            max_lading = max(max_lading + taak.brengen.aantal(self._auto_type), eindlading)
            if toevoeg_taken[0][-2] < t_max:
                t_max = toevoeg_taken[0][-2]
            starttijd_route = self.start_tijd

            # taak weghalen uit taken
            nog_te_plannen_taken.remove(taak)

        self._status = Status.FINISHED

    def vooraan_toe_te_voegen(self, nog_te_plannen_taken: list[Taak], eerste_taak: Taak, laatste_taak: Taak, max_wegbrengen: int, max_ophalen: int) -> Optional[Tuple[Taak, Long_time, Long_time]]:
        """
        Geeft de goedkoopste taak die vooraan aan de route kan worden toegevoegd.
        
        Parameters:
            nog_te_plannen_taken (list[Taak]): Lijst met taken die nog in een route moeten komen.
            eerste_taak (Taak): Eerste taak in de route.
            laatste_taak (Taak): Laatste taak in de route.
            max_wegbrengen (int): Maximale hoeveelheid die bij het ziekenhuis afgeleverd kan worden.
            max_ophalen (int): Maximale hoeveelheid die bij het ziekenhuis opgehaald kan worden.
        
        Returns:
            Optional[list[Taak, Long_time, Long_time]]: Taak die voor de route kan worden toegevoegd 
                                                        de bijbehorende starttijd of None als er geen taak voor kan worden toegevoegd
                                                        de maximale tijd waarop de route terug bij de hub moet zijn om op tijd de schoongemaakte instrumenten van deze taak te kunnen leveren
        """
        # alleen taken voor eerste_taak en met toegestane hoeveelheid brengen en ophalen
        gefilterd = [taak for taak in nog_te_plannen_taken if taak.tijdslot.starttijd < eerste_taak.begintijd_taak and taak.brengen.aantal(self._auto_type) <= max_wegbrengen and taak.halen.aantal(self._auto_type) <= max_ophalen]

        # sorteren op kosten van toevoegen taak voor eerste_taak
        gefilterd.sort(key = lambda taak: eerste_taak.cost_with_taak(taak, self._distances, self._auto_type, False))

        tijd_terug_hub = laatste_taak.eindtijd_taak + self._distances.get_time(laatste_taak.ziekenhuis, self._start_hub)
        for taak in gefilterd:
            reistijd = self._distances.get_time(taak.ziekenhuis, eerste_taak.ziekenhuis)
            max_starttijd = eerste_taak.begintijd_taak - reistijd - taak.laadtijd
            if taak.tijdslot.starttijd > max_starttijd:
                # starttijd van taak moet voor maximale tijdslot liggen
                continue # volgende taak bekijken
            reistijd_van_hub = self._distances.get_time(self._start_hub, taak.ziekenhuis)
            t_max_taak = taak.returntijd.eindtijd - Constants.TIJDSDUUR_SCHOONMAAK - reistijd_van_hub
            if t_max_taak < tijd_terug_hub:
                # route moet optijd terug zijn om genoeg tijd te geven voor schoonmaak
                continue # volgende taak bekijken
            # starttijd bepalen
            starttijd = max_starttijd + taak.laadtijd
            if starttijd > taak.tijdslot.eindtijd:
                # tijdvak eindigd voor maximale eindttijd, dus eindtijd tijdslot wordt eindtijd
                starttijd = taak.tijdslot.eindtijd - taak.laadtijd
            if tijd_terug_hub - (starttijd - reistijd_van_hub) > Constants.MAX_TIJDSDUUR_ROUTE:
                # toevoegen van taak zorgt voor te lange route
                continue
            # taak voldoet aan alle criteria
            taak_vooraan = taak
            return taak_vooraan, starttijd, t_max_taak
        return None, None, None

    def achteraan_toe_te_voegen(self, nog_te_plannen_taken: list[Taak], laatste_taak: Taak, max_wegbrengen: int, max_ophalen: int, t_max: Long_time, starttijd_route: Long_time) -> Optional[Tuple[Taak, Long_time, Long_time]]:
        """
        Geeft de goedkoopste taak die achteraan aan de route kan worden toegevoegd.
        
        Parameters:
            nog_te_plannen_taken (list[Taak]): Lijst met taken die nog in een route moeten komen.
            laatste_taak (Taak): Laatste taak in de route.
            max_wegbrengen (int): Maximale hoeveelheid die bij het ziekenhuis afgeleverd kan worden.
            max_ophalen (int): Maximale hoeveelheid die bij het ziekenhuis opgehaald kan worden.
            t_max (Long_time): De uiterlijke tijd waarop er bij een ziekenhuis moet worden vertrokken om op tijd terug te zijn om de al opgehaalde instrumenten op tijd schoon te maken. 
            starttijd_route (Long_time): De starttijd van huidige route
        
        Returns:
            Optional[list[Taak, Long_time, Long_time]]: Taak die voor de route kan worden toegevoegd 
                                                        de bijbehorende starttijd of None als er geen taak voor kan worden toegevoegd
                                                        de maximale tijd waarop de route terug bij de hub moet zijn om op tijd de schoongemaakte instrumenten van deze taak te kunnen leveren
        """
        # alleen taken voor eerste_taak en met toegestane hoeveelheid brengen en ophalen
        gefilterd = [taak for taak in nog_te_plannen_taken if taak.tijdslot.eindtijd > laatste_taak.eindtijd_taak and taak.brengen.aantal(self._auto_type) <= max_wegbrengen and taak.halen.aantal(self._auto_type) <= max_ophalen]
        
        # sorteren op kosten van toevoegen taak voor eerste_taak
        gefilterd.sort(key = lambda taak: laatste_taak.cost_with_taak(taak, self._distances, self._auto_type, True))

        for taak in gefilterd:
            reistijd = self._distances.get_time(laatste_taak.ziekenhuis, taak.ziekenhuis)
            min_eindtijd = laatste_taak.eindtijd_taak + reistijd + taak.laadtijd
            starttijd = laatste_taak.eindtijd_taak + reistijd
            if taak.tijdslot.eindtijd < min_eindtijd:
                # eindtijd van taak moet na maximale tijdslot liggen
                continue # volgende taak bekijken
            reistijd_terug_hub = self._distances.get_time(taak.ziekenhuis, self._start_hub)
            t_max_taak = taak.returntijd.eindtijd - Constants.TIJDSDUUR_SCHOONMAAK - self._distances.get_time(self._start_hub, taak.ziekenhuis)
            if t_max_taak < min_eindtijd + reistijd_terug_hub:
                # route moet optijd terug zijn om genoeg tijd te geven voor schoonmaak (vroegste tijd terug bij hub > maximale vertrektijd bij hub van return)
                continue # volgende taak bekijken
            if taak.tijdslot.starttijd > min_eindtijd - taak.laadtijd:
                # start tijdslot ligt na minimale starttijd -> starttijd wordt start tijdslot
                starttijd = taak.tijdslot.starttijd
                tijd_terug_hub = taak.tijdslot.starttijd + taak.laadtijd + reistijd_terug_hub 
                if t_max_taak < tijd_terug_hub:
                    # route moet optijd tureg zijn om genoeg tijd te geven voor schoonmaak
                    continue
            if starttijd + taak.laadtijd > t_max:
                # toevoegen zorgt dat instrumenten van route niet op tijd terug zijn om schoongemaakt te worden
                continue
            elif (starttijd + taak.laadtijd + reistijd_terug_hub) - starttijd_route > Constants.MAX_TIJDSDUUR_ROUTE:
                # toevoegen van taak zorgt voor te lange route
                continue
            # taak voldoet aan alle criteria
            return taak, starttijd, t_max_taak
        return None, None, None

    @property
    def start_tijd(self) -> Optional[Long_time]:
        if not self._taken:
            return None
        reistijd_vanaf_hub = self._distances.get_time(self._start_hub, self._taken[0].ziekenhuis)
        start_tijd = self._taken[0].begintijd_taak - reistijd_vanaf_hub
        return start_tijd
    
    @property
    def eind_tijd(self) -> Long_time:
        if not self._taken:
            return None
        reistijd_naar_hub = self._distances.get_time(self._taken[-1].ziekenhuis, self._start_hub)
        eind_tijd = self._taken[-1].eindtijd_taak + reistijd_naar_hub
        return eind_tijd
    
    @property
    def tijdslot(self) -> Tijdslot:
        if not self._taken:
            return None
        return Tijdslot(self.start_tijd, self.eind_tijd)

    @property
    def status(self) -> Status:
        return self._status
    
    @property
    def taken(self) -> List["Taak"]:
        """
        Geeft de taken van de route gesorteerd op starttijd van de taak.
        """
        self._taken.sort(key = lambda taak: taak.begintijd_taak)
        return self._taken
    
    @property
    def start_hub(self) -> "Hub":
        """
        Geeft de hub waar de route start en eindigd.
        """
        return self._start_hub
    
    @property
    def capaciteit(self):
        """
        Geeft de capaciteit van het voertuig waarin de route gereden wordt.
        """
        return self._capaciteit
    
    @property
    def auto_type(self):
        """
        Geeft het type voertuig waarin de route gereden wordt.
        """
        return self._auto_type
    
    @property
    def fits_bestelbus(self) -> bool:
        """
        Kijkt of de route in een bestelbus past.
        """
        for taak in self.taken:
            if taak.ziekenhuis.voorkeur_bak_kar == Bak_kar_voorkeur.KAR:
                # een taak in de route heeft voorkeur voor karren, dus bestelbus kan niet
                return False
        
        max_brenglading, max_haallading = self.max_lading(Auto_type.BESTELBUS)
        if max(max_brenglading, max_haallading) > Constants.capaciteit_auto(Auto_type.BESTELBUS):
            # de lading van de route overschrijdt de capaciteit van een bestelbus
            return False
        
        return True

    def set_auto_type(self, auto_type: Auto_type) -> None:
        """
        Veranderd het type voertuig waarin de route gereden wordt.

        Parameters:
            auto_type (Auto_type): Het type auto waarin de route gereden moet worden.

        Raises:
            ValueError: Als de route niet in het gekozen auto-type kan.
        """
        if auto_type == Auto_type.BAKWAGEN:
            self._auto_type = auto_type
        elif self.fits_bestelbus == False:
            raise ValueError("Een taak heeft een kar-voorkeur of de lading is te groot, dus kan de route niet in een bestelbus")
        else:
            self._auto_type = auto_type

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
        total_distance += self._distances.get_distance(self._start_hub, self._taken[0].ziekenhuis)
        for i in range(len(self._taken) - 1):
            total_distance += self._distances.get_distance(self._taken[i].ziekenhuis, self._taken[i + 1].ziekenhuis)
        total_distance += self._distances.get_distance(self._taken[-1].ziekenhuis, self._start_hub)
        return total_distance

    @property
    def total_time(self) -> float:
        """
        Bereken de totale tijd van de route in minuten.
        
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
        
        distance_cost = Cost.calculate_cost_distance(self.total_distance, self._auto_type)
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
            
    @property
    def arrival_times(self) -> List[Tuple["Taak", Long_time]]:
        """
        Bepaal de aankomsttijden bij het ziekenhuis van elke taak (niet per se de tijd dat taak wordt gestart)

        Returns:
            List[Tuple[Taak, Long_time]]: de aankomsttijden bij de ziekenhuizen van de taken in de route
        """
        if not self._taken:
            return []
        
        arrival_times = []
        arrival_times.append([self._taken[0], self.start_tijd + self._distances.get_time(self._start_hub, self._taken[0].ziekenhuis)])
        for i in range(len(self._taken) - 1):
            traveltime = self._distances.get_time(self._taken[i].ziekenhuis, self._taken[i + 1].ziekenhuis)
            arrival_times.append([self._taken[i + 1], self._taken[i].eindtijd_taak + traveltime])

        return arrival_times
    
    @property
    def travel_distances(self) -> List[list["Taak", "Taak", Long_time]]:
        """
        Bepaal de reisafstanden tussen de ziekenhuizen van elke taak 

        Returns:
            List[Tuple[Taak, taak, Long_time]]: de reisafstanden tussen de ziekenhuizen van de taken in de route
        """
        if not self._taken:
            return []
        
        travel_times = []
        for i in range(len(self._taken) - 1):
            traveltime = self._distances.get_distance(self._taken[i].ziekenhuis, self._taken[i + 1].ziekenhuis)
            travel_times.append([self._taken[i], self._taken[i + 1], traveltime])

        return travel_times

    @property
    def waiting_times(self) -> List[Tuple["Taak", Long_time]]:
        """
        Bepaal de wachttijd van de chauffeur voor hij aan de geplande taak kan beginnen nadat hij is gearriveerd

        Returns:
            List[Tuple["Taak", Long_time]]: de wachttijd van de chauffeur bij elke taak
        """
        if not self._taken:
            return []
        
        waiting_times = []
        for taak, arrival_time in self.arrival_times:
            waiting_times.append([taak, taak.begintijd_taak - arrival_time])
        return waiting_times
    
    @property
    def total_waiting_time(self) -> Long_time:
        """
        Bepaal de totale wachttijd van de chauffeur voor hij aan de geplande taken kan beginnen nadat hij is gearriveerd

        Returns:
            Long_time: de totale wachttijd van de chauffeur
        """
        if not self._taken:
            return Long_time(0)
        
        waiting_time = sum([float(waittime) for _, waittime in self.waiting_times])
        return Long_time(waiting_time)
    
    def max_lading_vrij(self, auto_type: Auto_type) -> Tuple[int, int]:
        """
        Bepaal de maximale ruimte die vrij is tijdens de route, oftewel maximale lading die nog aan route toegevoegd kan worden

        Returns:
            Tuple[int, int]: de maximale vrije ruimte voor wegbrengen, de maximale vrije ruimte voor ophalen
        """
        if not self._taken:
            return self._capaciteit, self._capaciteit
        
        startlading: int = 0
        eindlading: int = 0
        max_lading: int = 0
        for taak in self._taken:
            startlading += taak.brengen.aantal(auto_type)
            eindlading += taak.halen.aantal(auto_type)
            max_lading = max(max_lading + taak.brengen.aantal(auto_type), eindlading)
            max_wegbrengen = self._capaciteit - max_lading
            max_ophalen = self._capaciteit - eindlading

        return max_wegbrengen, max_ophalen
    
    def max_lading(self, auto_type: Auto_type) -> Tuple[int, int]:
        """
        Bepaal de maximale lading tijdens de route

        Returns:
            Tuple[int, int]: de maximale hoeveelheid die weggebracht wordt, de maximale hoeveelheid die opgehaald wordt
        """
        max_lading_vrij = self.max_lading_vrij(auto_type)
        return self._capaciteit - max_lading_vrij[0], self._capaciteit - max_lading_vrij[1]
    
    @property
    def max_eindtijd(self) -> Long_time:
        """
        Bepaal de maximale eindtijd van de route, waarop de route op het laatst terug op de hub moet zijn

        Returns:
            Long_time: de maximale eindtijd
        """
        max_eindttijd = max([taak.returntijd.eindtijd for taak in self._taken])
        return max_eindttijd
    
    @property
    def verschuiven(self) -> tuple[Long_time, Long_time]:
        """
        Bepaal de maximale tijd die de route naar voren en naar achteren geschoven kan worden zonder buiten de tijdvakken bij de ziekenhuizen aan te komen.

        Returns:
            tuple[Long_time, Long_time]: de maximale tijd dat route naar voren, naar achteren geschoven kan worden.
        """
        voor = [taak.begintijd_taak - taak.tijdslot.starttijd for taak in self.taken]
        achter = [taak.tijdslot.eindtijd - taak.eindtijd_taak for taak in self.taken]
        return min(voor), min(achter)
