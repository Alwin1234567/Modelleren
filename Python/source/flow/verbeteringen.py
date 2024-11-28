from warnings import warn
from source.locations import Hub
from source.structures import Status
from copy import deepcopy
import time
from tqdm import tqdm

class Verbeteringen:
    def __init__(self, hubs: list[Hub], initial_heat: float = 1, heat_reduction: float = 0.95, cooling_interval:int = 100) -> None:
        """
        Initialiseer de Verbeteringen class en controleer de status en routes van de hubs.

        Parameters:
            hubs (list): Een lijst van hubs.
            initial_heat (float): De initiële warmte voor het simuleren van annealing.
            heat_reduction (float): De factor waarmee de warmte wordt verminderd.
            cooling_interval (int): Het aantal iteraties waarna de warmte wordt verminderd.
        """
        self._status = Status.PREPARING
        self._hubs = []
        self.check_hubs_status(hubs)
        self.check_hubs_routes(hubs)
        self._hubs = hubs
        self._initial_heat = initial_heat
        self._heat = initial_heat
        self._heat_reduction = heat_reduction
        self._cooling_interval = cooling_interval
        self._iteration = 0

    def check_hubs_status(self, hubs: list[Hub]) -> None:
        """
        Controleer de status van de hubs en verzamel de namen van de hubs die niet klaar zijn.
    
        Parameters:
            hubs (list): Een lijst van hubs.
    
        Raises:
            ValueError: Als niet alle hubs klaar zijn voor verbeteringen.
        """
        failed_hubs = [hub.name for hub in hubs if hub.status != Status.FINISHED]
        
        if failed_hubs:
            raise ValueError(f"Niet alle hubs zijn klaar voor verbeteringen: {', '.join(failed_hubs)}")

    def check_hubs_routes(self, hubs: list[Hub]) -> None:
        """
        Controleer of alle hubs routes hebben. Geef een waarschuwing als sommige hubs geen routes hebben.
        Geef een foutmelding als geen enkele hub routes heeft.

        Parameters:
            hubs (list): Een lijst van hubs.

        Raises:
            ValueError: Als geen enkele hub routes heeft.
        """
        hubs_without_routes = [hub.name for hub in hubs if not hub.routes]
        
        if len(hubs_without_routes) == len(hubs):
            raise ValueError("Geen enkele hub heeft routes.")
        elif hubs_without_routes:
            warn(f"Sommige hubs hebben geen routes: {', '.join(hubs_without_routes)}")

    def verbeteringen(self) -> None:
        """
        Voer verbeteringen uit op de hubs.
        """
        if self.status != Status.PREPARING:
            raise ValueError("De verbeteringen zijn al uitgevoerd.")
        self._status = Status.CALCULATING
        for i, hub in enumerate(self._hubs):
            original_route_count = len(hub.routes)
            best_cost = hub.cost
            best_hub = deepcopy(hub)
            best_iteration = 0

             # Calculate the maximum allowed time in seconds
            max_time = original_route_count * 60
            start_time = time.time()

            # Initialize the progress bar
            progress_bar = tqdm(total=max_time, desc=f"Improving hub {hub.name}", unit="s")

            while self._heat > 0:
                hub.split_routes_waittime(self._heat)
                hub.combine_routes(self._heat)
                hub.split_routes_distance(self._heat)
                hub.combine_routes(self._heat)
                
                self._cool_down()

                # check if the cost has decreased
                current_cost = hub.cost
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_iteration = self._iteration
                    best_hub = deepcopy(hub)
                
                if self._iteration - best_iteration > 100:
                    break

                # Check if the elapsed time exceeds the maximum allowed time
                elapsed_time = time.time() - start_time
                if elapsed_time > max_time:
                    break

                # Update the progress bar
                progress_bar.n = int(elapsed_time)
                progress_bar.refresh()
            
            # Close the progress bar
            progress_bar.close()

            self._hubs[i] = best_hub
            self._heat = self._initial_heat
            self._itteration = 0
        self._status = Status.FINISHED

    def _cool_down(self) -> None:
        """
        Verminder de warmte na een bepaald aantal iteraties.
        """
        self._iteration += 1
        if self._iteration % self._cooling_interval == 0:
            self._heat *= self._heat_reduction


    @property
    def hubs(self) -> list[Hub]:
        """
        De hubs.

        Returns:
            list: Een lijst van hubs.
        """
        return self._hubs
    
    @property
    def status(self) -> Status:
        """
        De status van de verbeteringen.

        Returns:
            Status: De status van de verbeteringen.
        """
        return self._status
