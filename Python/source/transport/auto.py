from .route import Route
from source.structures import ID, Tijdslot
from typing import List
import numpy as np

class Auto:
    """
    Een auto die routes kan rijden.
    """

    def __init__(self) -> None:
        """
        Maak een nieuwe auto aan.
        """
        self._id = ID()
        self._routes: list[Route] = []

    def heeft_route_overlap(self, route: Route) -> bool:
        """
        Check of de auto een bepaald route type heeft.
        
        Parameters:
            route_type (Route_type): Het route type dat moet worden gecheckt.
        
        Returns:
            bool: True als de auto het route type heeft, anders False.
        """
        for eigen_route in self._routes:
            if eigen_route.tijdslot.overlap(route.tijdslot):
                return True
        return False
    
    def tijdverschil(self, route) -> int:
        """
        Bereken het minimale tijdverschil tussen de gegeven route en de routes van de auto.

        Parameters:
            route (Route): De route waarvan het tijdverschil moet worden berekend.

        Returns:
            int: Het minimale tijdverschil in minuten tussen de gegeven route en de routes van de auto.
        """
        if self.heeft_route_overlap(route):
            return np.inf
        
        tijdverschillen = []
        for eigen_route in self._routes:
            tijdverschillen.append(eigen_route.tijdslot.tijdverschil(route.tijdslot))
        return min(tijdverschillen)
    
    def add_route(self, route: Route) -> None:
        """
        Voeg een route toe aan de auto.
        
        Parameters:
            route (Route): De route die moet worden toegevoegd.
        
        Raises:
            ValueError: Als de route al in de auto zit.
        """
        if self.heeft_route_overlap(route):
            raise ValueError("De route overlap met een bestaande route.")
        if route in self._routes:
            raise ValueError("De route zit al in de auto.")
        self._routes.append(route)
    
    @property
    def tijdsloten(self) -> List[Tijdslot]:
        """
        De tijdsloten van de routes van de auto.
        
        Returns:
            List[Tijdslot]: De tijdsloten van de routes van de auto.
        """
        return [route.tijdslot for route in self._routes]
    
    @property
    def id(self) -> ID:
        """
        Het ID van de auto.

        Returns:
            ID: Het ID van de auto.
        """
        return self._id
        
    @property
    def routes(self) -> list[Route]:
        """
        De routes van de auto gesorteerd op vertrektijd.
        
        Returns:
            List[Route]: De routes van de auto.
        """
        self._routes.sort(key = lambda route: route.start_tijd)
        return self._routes
