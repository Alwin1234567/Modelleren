from .location import Location, Location_type
from .ziekenhuis import Ziekenhuis
from source.structures import Status, Distances, Taak
from source.transport import Route
import pandas as pd
from tqdm import tqdm

class Hub(Location):

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, Location_type.HUB, **kwargs)
        self._status = Status.PREPARING
        self._distances = Distances()
        self._distances.add_location(self)
        self._routes: list[Route] = []
    

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
            
            route = Route(self, self._distances)
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
            Taak: De starttaak met de hoogste halen_brengen waarde en de kortste tijdslot bij gelijke halen_brengen.
        """
        if not taken:
            raise ValueError("De lijst van taken is leeg.")
    
        # Sort the taken list by halen_brengen in descending order and by tijdslot duration in ascending order
        taken.sort(key=lambda taak: (-taak.halen_brengen, len(taak.tijdslot)))
    
        return taken[0]

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
