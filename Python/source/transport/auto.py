from .route import Route, Route_type
from source.structures import ID
from typing import Dict, List

class Auto:
    """
    Een auto die routes kan rijden.
    """

    def __init__(self) -> None:
        """
        Maak een nieuwe auto aan.
        """
        self._id = ID()
        self._routes: Dict[Route_type, Route] = {}

    def has_route_type(self, route_type: Route_type) -> bool:
        """
        Check of de auto een bepaald route type heeft.
        
        Parameters:
            route_type (Route_type): Het route type dat moet worden gecheckt.
        
        Returns:
            bool: True als de auto het route type heeft, anders False.
        """
        return route_type in set(self.route_types)
    
    def add_route(self, route: Route) -> None:
        """
        Voeg een route toe aan de auto.
        
        Parameters:
            route (Route): De route die moet worden toegevoegd.
        
        Raises:
            ValueError: Als de route al in de auto zit.
        """
        if route.route_type in self._routes.keys():
            raise ValueError("Auto already has a route of this type")
        if route in set(self._routes.values()):
            raise ValueError("Route is already in auto")
        self._routes[route.route_type] = route

    
    
    @property
    def route_types(self) -> List[Route_type]:
        return list(self._routes.keys())
    
    @property
    def id(self) -> ID:
        return self._id
