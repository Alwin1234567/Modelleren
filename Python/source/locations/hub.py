from .location import Location, Coordinates, Location_type

class Hub(Location):

    def __init__(self, name: str) -> None:
        super().__init__(name, Location_type.HUB)   
    
