from .location import Location, Coordinates, Location_type

class Hub(Location):

    def __init__(self, name: str, coordinates: Coordinates) -> None:
        super().__init__(coordinates, name, Location_type.HUB)   
    
