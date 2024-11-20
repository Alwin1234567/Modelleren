from .location import Location, Location_type
from .ziekenhuis import Ziekenhuis
from source.structures import Status, Distances, Taak, Auto_type, Bak_kar_voorkeur
from source.transport import Route, Auto
import pandas as pd
from tqdm import tqdm
from warnings import warn
from source.constants import Constants

class Hub(Location):

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, Location_type.HUB, **kwargs)
        self._status = Status.PREPARING
        self._distances = Distances()
        self._distances.add_location(self)
        self._routes: list[Route] = []
        self._autos: list[Auto] = []

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
    
    def empty_autos(self) -> None:
        if self._autos:
            warn(f"De autos van hub {self.name} worden geleegd. Dit waren {len(self._autos)} auto's", RuntimeWarning)
        self._autos = []

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
        
        # beide soorten auto's vullen met routes van dat type auto
        self._fill_autos_type(Auto_type.BAKWAGEN)
        self._fill_autos_type(Auto_type.BESTELBUS)
        
    
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
        self._autos.append(Auto(auto_type)) 
        self._autos[0].add_route(nog_te_plannen_routes[0])

        for route in nog_te_plannen_routes[1:]:
            ingepland = False
            self._autos.sort(key = lambda auto: auto.routes[-1].eind_tijd)
            for auto in self._autos:
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
        return self._autos
    
    def add_routes(self, route: Route) -> None:
        """
        Voeg een route toe aan de hub

        Parameters:
            route (Route): Een route object dat aan de hub moet worden toegevoegd
        """
        self._routes = route
