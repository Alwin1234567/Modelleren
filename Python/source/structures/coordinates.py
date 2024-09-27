class Coordinates:
    def __init__(self, lat, lon) -> None:
        self._lat = lat
        self._lon = lon
    
    def __str__(self) -> str:
        return f"({self.lat}, {self.lon})"

    @property
    def lat(self):
        return self._lat
    
    @property
    def lon(self):
        return self._lon
    
    @property
    def coordinates(self):
        return (self.lat, self.lon)
