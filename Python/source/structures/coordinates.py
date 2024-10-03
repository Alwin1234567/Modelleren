class Coordinates:
    """
    Een class om coördinaten te representeren.

    Attributen:
        lat (float): De breedtegraad.
        lon (float): De lengtegraad.
    """

    def __init__(self, lat, lon) -> None:
        """
        Initialiseer een nieuw Coordinates object.

        Args:
            lat (float): De breedtegraad.
            lon (float): De lengtegraad.
        """
        self._lat = lat
        self._lon = lon
    
    def __str__(self) -> str:
        """
        Retourneer een stringrepresentatie van de coördinaten.

        Returns:
            str: De coördinaten in de vorm (lat, lon).
        """
        return f"({self.lat}, {self.lon})"

    @property
    def lat(self):
        """
        Haal de breedtegraad op.

        Returns:
            float: De breedtegraad.
        """
        return self._lat
    
    @property
    def lon(self):
        """
        Haal de lengtegraad op.

        Returns:
            float: De lengtegraad.
        """
        return self._lon
    
    @property
    def coordinates(self):
        """
        Haal de coördinaten op als een tuple.

        Returns:
            tuple: De coördinaten in de vorm (lat, lon).
        """
        return (self.lat, self.lon)

    @property
    def OSRM_str(self):
        """
        Haal de coördinaten op in een stringformaat geschikt voor OSRM.

        Returns:
            str: De coördinaten in de vorm "point=lat,lon".
        """
        return f"point={self.lat},{self.lon}"
    