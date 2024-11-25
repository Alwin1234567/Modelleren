from .location import Location, Location_type
from .ziekenhuis import Ziekenhuis
from source.structures import Status, Distances, Taak, Auto_type, Bak_kar_voorkeur, Cost, Long_time
from source.transport import Route, Auto
import pandas as pd
from tqdm import tqdm
from warnings import warn
from source.constants import Constants
from datetime import time
import random

class Hub(Location):

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, Location_type.HUB, **kwargs)
        self._status = Status.PREPARING
        self._distances = Distances()
        self._distances.add_location(self)
        self._routes: list[Route] = []
        self._autos: list[Auto] = []
        self._auto_status = Status.PREPARING

    def add_ziekenhuis(self, ziekenhuis: Ziekenhuis) -> None:
        """
        Voeg een ziekenhuis toe aan de hub.
        """
        if self._status != Status.PREPARING:
            raise Exception("Het is niet mogelijk om een ziekenhuis toe te voegen aan een hub die niet in de status 'PREPARING' is.")
        self._distances.add_location(ziekenhuis)
    
    def finish_creation(self) -> None:
        """
        Ronde de creatie van de hub af.
        """
        if self._status != Status.PREPARING:
            raise Exception("Het is niet mogelijk om de creatie van een hub af te ronden die niet in de status 'PREPARING' is.")
        self._status = Status.CALCULATING
        self._distances.generate_distances()
        self._calculate_routes()
        self._status = Status.FINISHED
    
    def _calculate_routes(self) -> None:
        """
        Bereken de routes van de hub naar de ziekenhuizen.
        """
        if self._status != Status.CALCULATING:
            raise Exception("Het is niet mogelijk om de routes te berekenen als de status niet 'CALCULATING' is.")
        
        remaining_taken = [taak for ziekenhuis in self.ziekenhuizen for taak in ziekenhuis.taken]
        total_taken = len(remaining_taken)
        progress_bar = tqdm(total=total_taken, desc=f"Calculating routes for hub {self.name}", unit="taak")

        while remaining_taken:
            initial_length = len(remaining_taken)
            
            # Bij de startoplossing alle voertuigen bakwagens
            route = Route(self, self._distances, Auto_type.BAKWAGEN)
            starttaak = self._choose_starttaak(remaining_taken)
            remaining_taken.remove(starttaak)
            route.maak_route(starttaak, remaining_taken)
            self._routes.append(route)
            
            remaining_taken = [taak for taak in remaining_taken if taak not in route.taken]
            
            final_length = len(remaining_taken)
            
            if final_length >= initial_length:
                raise Exception("De lengte van remaining_taken is niet afgenomen. Er is mogelijk een probleem met de routeberekening.")
            
            # Update the progress bar
            progress_bar.update(initial_length - final_length)
        
        progress_bar.close()

    def _choose_starttaak(self, taken: list[Taak]) -> Taak:
        """
        Kies de starttaak van de route.
    
        Parameters:
            taken (list[Taak]): De lijst van taken waaruit de starttaak gekozen moet worden.
    
        Returns:
            Taak: De starttaak met de hoogste halen_brengen_sets waarde en de kortste tijdslot bij gelijke halen_brengen_sets.
        """
        if not taken:
            raise ValueError("De lijst van taken is leeg.")
    
        # Sort the taken list by halen_brengen_sets in descending order and by tijdslot duration in ascending order
        taken.sort(key=lambda taak: (-taak.halen_brengen_sets, len(taak.tijdslot)))
    
        return taken[0]
    
    def add_route(self, route: Route) -> None:
        """
        Voeg een route toe aan de hub

        Parameters:
            route (Route): Een route object dat aan de hub moet worden toegevoegd
        """
        self._routes.append(route)

    def remove_route(self, route: Route) -> None:
        """
        Verwijderd een route uit de hub

        Parameters:
            route (Route): Een route object dat uit de hub moet worden verwijderd
        """
        if route.taken:
            # staan nog taken in route, dus waarschuwing geven bij verwijderen route
            warn("Er wordt een route verwijderd waar nog taken in staan.", RuntimeWarning)
        self._routes.remove(route)
    
    def split_routes_waittime(self, kans: float = 0) -> None:
        """
        Splits routes in twee op de langste wachttijd als dit goedkoper is
        """
        if not self._routes:
            # geen routes in de hub
            warn("Er zijn geen routes om te splitsen.", RuntimeWarning)
            return None 
        
        for route in self.routes:
            sorted_waittime = route.waiting_times
            sorted_waittime.sort(key = lambda taak_time: taak_time[1], reverse = True)
            if sorted_waittime[0][1] < Long_time(time(second = 5)):
                # grootste wachttijd is korter dan 5 seconden, door afrondcorrectie of door één taak in route
                continue
            
            # taak met langste wachttijd en taak daarvoor zoeken (hiertussen komt mogelijk de splitsing)
            taak_B = sorted_waittime[0][0]
            index_longest_waittime = route.taken.index(taak_B)
            taak_A = route.taken[index_longest_waittime - 1]
            gap = taak_B.begintijd_taak - taak_A.eindtijd_taak
            
            # kosten van huidige routestuk A - B
            distance_cost_A_B = Cost.calculate_cost_distance(self._distances.get_distance(taak_A.ziekenhuis, taak_B.ziekenhuis), route.auto_type)
            time_cost_A_B = Cost.calculate_cost_time(taak_A.eindtijd_taak.tijd, float(gap))
            cost_A_B = distance_cost_A_B + time_cost_A_B
            
            # reistijd van A-Hub en Hub-B
            cost_A_hub = self._distances.get_distance_time(taak_A.ziekenhuis, self).cost(taak_A.eindtijd_taak.tijd, route.auto_type)
            distancetime_hub_B = self._distances.get_distance_time(self, taak_B.ziekenhuis)
            cost_hub_B = distancetime_hub_B.cost((taak_B.begintijd_taak - distancetime_hub_B.time).tijd, route.auto_type)
            cost_A_hub_B = cost_A_hub + cost_hub_B
            
            if cost_A_hub_B < cost_A_B or random.random() < kans:
                # goedkoper om te splitsen, dus splitsing uitvoeren
                self._split_route(index_longest_waittime, route)

    def split_routes_distance(self, kans: float = 0) -> None:
        """
        Splits routes in twee op de langste reisafstand als dit goedkoper is
        """
        if not self._routes:
            # geen routes in de hub
            warn("Er zijn geen routes om te splitsen.", RuntimeWarning)
            return None 
        
        for route in self.routes:
            if len(route.taken) < 2:
                # route met maar één taak is niet te splitsen
                continue
            travel_distances = route.travel_distances
            travel_distances.sort(key = lambda taak_distance: taak_distance[2], reverse = True)

            if travel_distances[0][2] < 1:
                # kortste afstand is minder dan 1 meter, dus splitsen niet nodig
                continue
            
            # taken met langste reistijd ertussen zoeken (hiertussen komt mogelijk de splitsing)
            taak_A = travel_distances[0][0]
            taak_B = travel_distances[0][1]
            gap = taak_B.begintijd_taak - taak_A.eindtijd_taak
            
            # kosten van huidige routestuk A - B
            distance_cost_A_B = Cost.calculate_cost_distance(travel_distances[0][2], route.auto_type)
            time_cost_A_B = Cost.calculate_cost_time(taak_A.eindtijd_taak.tijd, float(gap))
            cost_A_B = distance_cost_A_B + time_cost_A_B
            
            # reistijd van A-Hub en Hub-B
            cost_A_hub = self._distances.get_distance_time(taak_A.ziekenhuis, self).cost(taak_A.eindtijd_taak.tijd, route.auto_type)
            distancetime_hub_B = self._distances.get_distance_time(self, taak_B.ziekenhuis)
            cost_hub_B = distancetime_hub_B.cost((taak_B.begintijd_taak - distancetime_hub_B.time).tijd, route.auto_type)
            cost_A_hub_B = cost_A_hub + cost_hub_B
            
            if cost_A_hub_B < cost_A_B or random.random() < kans:
                # goedkoper om te splitsen, dus splitsing uitvoeren
                self._split_route(route.taken.index(taak_B), route)

    def _split_route(self, split_index: int, route: Route) -> None:
        """
        Splits een route in 2 voor de taak met de meegegeven index.

        Parameters:
            split_index (int): De index van de taak waarvoor de splitsing plaatsvindt.
        """
        # na het splitsen moeten de auto's opnieuw ingedeeld worden
        self._auto_status = Status.PREPARING
        
        new_route = route.copy()
        self.add_route(new_route)

        taken = route.taken.copy()
        for i, taak in enumerate(taken):
            if i < split_index:
                # alle taken t/m taak_A verwijderen uit gekopieerde route
                new_route.remove_taak(taak)
            else:
                # alle taken vanaf taak_B verwijderen uit originele route
                route.remove_taak(taak)
    
    def combine_routes(self, kans: float = 0) -> None:
        """
        Plak routes aan elkaar als dit goedkoper is
        """
        # na het combineren moeten de auto's opnieuw ingedeeld worden
        self._auto_status = Status.PREPARING

        te_combineren_routes = self.routes.copy()

        while len(te_combineren_routes) > 1:
            # zolang er twee routes over zijn
            # random route kiezen om aan te plakken
            huidige_route = random.choice(te_combineren_routes) 
            te_combineren_routes.remove(huidige_route)
            
            # vooraan en achteraan toe te voegen routes opvragen
            vooraan = self.combine_before(huidige_route, te_combineren_routes)
            achteraan = self.combine_after(huidige_route, te_combineren_routes)
            passende_routes = vooraan + [route for route in achteraan if route not in vooraan]
            
            if not passende_routes:
                # geen routes die geplakt kunnen worden aan huidige
                continue

            toegevoegd = False
            while len(passende_routes) > 0 and not toegevoegd:
                # route random kiezen uit passende routes
                plak_route = random.choice(passende_routes)
                if plak_route in vooraan:
                    voorste_route = plak_route
                    achterste_route = huidige_route
                else:
                    voorste_route = huidige_route
                    achterste_route = plak_route
                   
                distance_time_routes = self._distances.get_distance_time(voorste_route.taken[-1].ziekenhuis, achterste_route.taken[0].ziekenhuis)

                # plaatsing van routes bepalen, zodat ze zo goed mogelijk op elkaar aansluiten
                originele_eindtijd_voorste = voorste_route.taken[-1].eindtijd_taak
                originele_starttijd_achterste = achterste_route.taken[0].begintijd_taak
                eind_voorste = (originele_eindtijd_voorste - voorste_route.verschuiven[0]) + distance_time_routes.time
                start_achterste = max(eind_voorste, (originele_starttijd_achterste - achterste_route.verschuiven[0]))
                eind_voorste = min(start_achterste, (originele_eindtijd_voorste + voorste_route.verschuiven[1]) + distance_time_routes.time)

                # negatieve verschuiving = eerder in de tijd, positieve verschuiving = later in de tijd
                verschuiving_voorste = eind_voorste - distance_time_routes.time - originele_eindtijd_voorste
                verschuiving_achterste = start_achterste - originele_starttijd_achterste

                # controleren maximale routetijd en maximale eindtijd
                duur_nieuwe_route = (achterste_route.eind_tijd + verschuiving_achterste) - (voorste_route.start_tijd + verschuiving_voorste)
                if duur_nieuwe_route > Constants.MAX_TIJDSDUUR_ROUTE:
                    # opnieuw route kiezen om met deze samen te voegen
                    passende_routes.remove(plak_route)
                    continue
                elif achterste_route.eind_tijd > achterste_route.max_eindtijd or achterste_route.eind_tijd > voorste_route.max_eindtijd:
                    # maximale eindttijd van een van beide routes wordt overschreden
                    passende_routes.remove(plak_route)
                    continue

                # kosten berekenen van originele en samengevoegde routes
                cost_oude_routes = voorste_route.total_cost + achterste_route.total_cost
                distance_cost = Cost.calculate_cost_distance(voorste_route.total_distance + achterste_route.total_distance + distance_time_routes.distance, voorste_route.auto_type)
                time_cost = Cost.calculate_cost_time((voorste_route.start_tijd + verschuiving_voorste).tijd, float(duur_nieuwe_route))
                cost_nieuwe_route = distance_cost + time_cost
                
                # als goedkoper toestaan of met bepaalde kans verslechteringen toestaan -> uitvoeren
                if cost_nieuwe_route < cost_oude_routes or random.random() < kans:
                    print('samenvoegen goedkoper:', cost_nieuwe_route < cost_oude_routes)
                    # voorste route verschuiven
                    for taak in voorste_route.taken:
                        taak.set_begintijd_taak(taak.begintijd_taak + verschuiving_voorste)
                    # taken uit achterste route toevoegen aan voorste route (en begintijd taak aanpassen)
                    for taak in achterste_route.taken:
                        taak.set_begintijd_taak(taak.begintijd_taak + verschuiving_achterste)
                        voorste_route.add_taak(taak)
                        achterste_route.remove_taak(taak)
                    # achterste (lege) route verwijderen en nieuwe samengevoegde route behouden
                    self.remove_route(achterste_route)
                    te_combineren_routes.remove(plak_route)
                    toegevoegd = True
                    
                else:
                    # de plak_route wordt niet geplakt, verder met nieuwe huidige_route
                    passende_routes.remove(plak_route)
                    break

    def combine_before(self, huidige_route: Route, te_combineren_routes: list[Route]) -> list[Route]:
        """
        Geeft routes die voor huidige_route geplaatst kunnen worden (na plaatsing nog wel maximale routeduur controleren)

        Parameters:
            huidige_route (Route): De route waarvoor een route geplakt moet worden.
            te_combineren_routes (list[Route]): Lijst met routes die nog gecombineerd kunnen worden.
        """
        voor_schuiven, achter_schuiven = huidige_route.verschuiven
        laatste_starttijd = huidige_route.taken[0].begintijd_taak + achter_schuiven # zonder reis van hub naar ziekenhuis, omdat andere route ervoor geplaatst wordt
        vroegste_eindtijd = huidige_route.eind_tijd - voor_schuiven # met reis van ziekenhuis naar hub, omdat andere route ervoor geplaatst wordt
        
        # filteren op: zelfde autotype, gezamelijke lading past in voertuig, maximale eindttijd niet overschreden, gezamelijke routelengte kleiner dan max
        gefilterd_1: list[Route] = [nieuwe_route for nieuwe_route in te_combineren_routes if nieuwe_route.auto_type == huidige_route.auto_type and \
                       nieuwe_route.max_lading(nieuwe_route.auto_type)[0] <= huidige_route.max_lading_vrij(huidige_route.auto_type)[0] and \
                       nieuwe_route.max_lading(nieuwe_route.auto_type)[1] <= huidige_route.max_lading_vrij(huidige_route.auto_type)[1] and \
                       vroegste_eindtijd <= nieuwe_route.max_eindtijd and \
                       (huidige_route.eind_tijd - huidige_route.taken[0].begintijd_taak) + (nieuwe_route.taken[-1].eindtijd_taak - nieuwe_route.start_tijd) <= Long_time(Constants.MAX_TIJDSDUUR_ROUTE)]
        if not gefilterd_1:
            return []
        
        # route-object, laatste starttijd, vroegste eindtijd, reistijd
        # gefilterd_2: list[list[Route, Long_time, Long_time, float]] = [[nieuwe_route, nieuwe_route.start_tijd + nieuwe_route.verschuiven[1], nieuwe_route.taken[-1].eindtijd_taak - nieuwe_route.verschuiven[0], self._distances.get_time(nieuwe_route.taken[-1].ziekenhuis, huidige_route.taken[0].ziekenhuis)] for nieuwe_route in gefilterd_1]
        gefilterd_2: list[list[Route, Long_time, Long_time, float]] = []
        for nieuwe_route in gefilterd_1:
            nieuw_laatste_starttijd: Long_time = nieuwe_route.start_tijd + nieuwe_route.verschuiven[1]
            nieuw_vroegste_eindtijd: Long_time = nieuwe_route.taken[-1].eindtijd_taak - nieuwe_route.verschuiven[0]
            reistijd: float = self._distances.get_time(nieuwe_route.taken[-1].ziekenhuis, huidige_route.taken[0].ziekenhuis)
            gefilterd_2.append([nieuwe_route, nieuw_laatste_starttijd, nieuw_vroegste_eindtijd, reistijd])

        # filteren op: samen mogelijk zonder overlap, minimale routeduur kleiner dan max, gezamelijke routelengte met reistijd kleiner dan max
        gefilterd_3 = [nieuwe_route for nieuwe_route, nieuw_laatste_starttijd, nieuw_vroegste_eindtijd, reistijd in gefilterd_2 if \
                       nieuw_vroegste_eindtijd + reistijd <= laatste_starttijd and \
                       vroegste_eindtijd - nieuw_laatste_starttijd <= Long_time(Constants.MAX_TIJDSDUUR_ROUTE) and \
                       (huidige_route.eind_tijd - huidige_route.taken[0].begintijd_taak) + (nieuwe_route.taken[-1].eindtijd_taak - nieuwe_route.start_tijd) + reistijd <= Long_time(Constants.MAX_TIJDSDUUR_ROUTE)]
        return gefilterd_3

    def combine_after(self, huidige_route: Route, te_combineren_routes: list[Route]) -> list[Route]:
        """
        Geeft routes die na huidige_route geplaatst kunnen worden (na plaatsing nog wel maximale routeduur controleren)

        Parameters:
            huidige_route (Route): De route waarna een route geplakt moet worden.
            te_combineren_routes (list[Route]): Lijst met routes die nog gecombineerd kunnen worden.
        """
        voor_schuiven, achter_schuiven = huidige_route.verschuiven
        laatste_starttijd = huidige_route.start_tijd + achter_schuiven # zonder reis van hub naar ziekenhuis, omdat andere route ervoor geplaatst wordt
        vroegste_eindtijd = huidige_route.taken[-1].eindtijd_taak - voor_schuiven # met reis van ziekenhuis naar hub, omdat andere route ervoor geplaatst wordt
        
        # filteren op: zelfde autotype, gezamelijke lading past in voertuig, maximale eindttijd niet overschreden, gezamelijke routelengte kleiner dan max
        gefilterd_1: list[Route] = [nieuwe_route for nieuwe_route in te_combineren_routes if nieuwe_route.auto_type == huidige_route.auto_type and \
                       nieuwe_route.max_lading(nieuwe_route.auto_type)[0] <= huidige_route.max_lading_vrij(huidige_route.auto_type)[0] and \
                       nieuwe_route.max_lading(nieuwe_route.auto_type)[1] <= huidige_route.max_lading_vrij(huidige_route.auto_type)[1] and \
                       nieuwe_route.taken[-1].eindtijd_taak - nieuwe_route.verschuiven[0] <= huidige_route.max_eindtijd and \
                       (huidige_route.eind_tijd - huidige_route.taken[0].begintijd_taak) + (nieuwe_route.taken[-1].eindtijd_taak - nieuwe_route.start_tijd) <= Long_time(Constants.MAX_TIJDSDUUR_ROUTE)]
        if not gefilterd_1:
            return []
        
        # route-object, laatste starttijd, vroegste eindtijd, reistijd
        gefilterd_2: list[list[Route, Long_time, Long_time, float]] = []
        for nieuwe_route in gefilterd_1:
            nieuw_laatste_starttijd: Long_time = nieuwe_route.start_tijd + nieuwe_route.verschuiven[1]
            nieuw_vroegste_eindtijd: Long_time = nieuwe_route.taken[-1].eindtijd_taak - nieuwe_route.verschuiven[0]
            reistijd: float = self._distances.get_time(huidige_route.taken[-1].ziekenhuis, nieuwe_route.taken[0].ziekenhuis)
            gefilterd_2.append([nieuwe_route, nieuw_laatste_starttijd, nieuw_vroegste_eindtijd, reistijd])

        # filteren op: samen mogelijk zonder overlap, minimale routeduur kleiner dan max, gezamelijke routelengte met reistijd kleiner dan max
        gefilterd_3 = [nieuwe_route for nieuwe_route, nieuw_laatste_starttijd, nieuw_vroegste_eindtijd, reistijd in gefilterd_2 if \
                       nieuw_laatste_starttijd - reistijd >= vroegste_eindtijd and \
                       nieuw_vroegste_eindtijd - laatste_starttijd <= Long_time(Constants.MAX_TIJDSDUUR_ROUTE) and \
                       (nieuwe_route.eind_tijd - nieuwe_route.taken[0].begintijd_taak) + (huidige_route.taken[-1].eindtijd_taak - huidige_route.start_tijd) + reistijd <= Long_time(Constants.MAX_TIJDSDUUR_ROUTE)]
        return gefilterd_3

    def switch_auto_type(self, kans: float = 0) -> None:
        """
        Wisselt het auto_type van routes.
        """
        # na het switchen moeten de auto's opnieuw ingedeeld worden
        self._auto_status = Status.PREPARING

        for route in self._routes:
            if route.auto_type == Auto_type.BAKWAGEN:
                if not route.fits_bestelbus:
                    continue
                type_nieuw = Auto_type.BESTELBUS
            else:
                type_nieuw = Auto_type.BAKWAGEN
            
            # alleen reiskosten vergelijken, omdat tijdsduur niet veranderd
            distance = route.total_distance
            distance_cost_oud = Cost.calculate_cost_distance(distance, route.auto_type)
            distance_cost_nieuw = Cost.calculate_cost_distance(distance, type_nieuw)
            # andere type goedkoper of met bepaalde kans -> type wisselen
            if distance_cost_oud > distance_cost_nieuw or random.random() < kans:
                route.set_auto_type(type_nieuw)

    def empty_autos(self) -> None:
        if self._autos:
            warn(f"De autos van hub {self.name} worden geleegd. Dit waren {len(self._autos)} auto's", RuntimeWarning)
        self._autos = []
        self._auto_status = Status.PREPARING

    def fill_autos(self) -> None:
        """
        Plaatst alle routes van de hub in auto's.
        """
        if not self._routes:
            # geen routes in de hub
            warn("Er kunnen geen auto's worden gevuld als er geen routes in de hub zijn.", RuntimeWarning)
            return None
        
        if self._autos:
            # auto's legen en opnieuw vullen
            self.empty_autos()
        
        self._auto_status = Status.CALCULATING
        # beide soorten auto's vullen met routes van dat type auto
        self._fill_autos_type(Auto_type.BAKWAGEN)
        self._fill_autos_type(Auto_type.BESTELBUS)

        self._auto_status = Status.FINISHED
        
    
    def _fill_autos_type(self, auto_type: Auto_type) -> bool:
        """
        Vult auto's met routes met dat specifieke type auto.

        Parameters:
            auto_type (Auto_type): Het type auto dat gevuld moet worden.
        
        Returns:
            bool: True als auto's zijn toegevoegd, False als er geen routes waren om aan auto's toe te voegen
        """
        # sorteer routes op starttijd 
        nog_te_plannen_routes = [route for route in self._routes if route.auto_type == auto_type]
        if len(nog_te_plannen_routes) == 0:
            # geen routes met dit type auto
            return False
        nog_te_plannen_routes.sort(key = lambda route: route.start_tijd)

        # eerste auto toevoegen aan hub met daarin eerste route
        nieuwe_auto = Auto(auto_type)
        nieuwe_auto.add_route(nog_te_plannen_routes[0])
        self._autos.append(nieuwe_auto) 

        for route in nog_te_plannen_routes[1:]:
            ingepland = False
            autos_dit_type = [auto for auto in self._autos if auto.auto_type == auto_type]
            autos_dit_type.sort(key = lambda auto: auto.routes[-1].eind_tijd)
            for auto in autos_dit_type:
                if auto.routes[-1].eind_tijd + Constants.WACHTTIJD_TUSSEN_ROUTES <= route.start_tijd:
                    # route toevoegen aan auto
                    auto.add_route(route)
                    ingepland = True
                    break
            
            if not ingepland:
                # route in nieuwe auto plaatsen
                nieuwe_auto = Auto(auto_type)
                nieuwe_auto.add_route(route)
                self._autos.append(nieuwe_auto) 
        return True

    @property
    def ziekenhuizen(self) -> list[Ziekenhuis]:
        """
        Geef de ziekenhuizen die aan de hub zijn toegevoegd.
        """
        return [location for location in self._distances.locations.values() if location.type == Location_type.ZIEKENHUIS]
    
    @property
    def distances(self) -> pd.DataFrame:
        """
        Geef de afstanden van de hub tot de andere locaties.
        """
        return self._distances.distances
    
    @property
    def status(self) -> Status:
        """
        Geef de status van de hub.
        """
        return self._status   
    
    @property
    def routes(self) -> list[Route]:
        """
        Geef de routes die aan de hub zijn toegevoegd.
        """
        return self._routes
    
    @property
    def autos(self) -> list[Auto]:
        """
        Geef de auto's die aan de hub zijn toegevoegd.
        """
        if self._auto_status != Status.FINISHED:
            # auto's vullen is nog niet gebeurd, dus eerst uitvoeren
            self.fill_autos()
        return self._autos
