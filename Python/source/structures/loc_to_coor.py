from geopy.geocoders import Nominatim
from .coordinates import Coordinates

class LocationToCoordinates:
    def __init__(self) -> None:
        self._adres = {'street': 'leidsestraatweg', 'country': 'Nederland'} #{'street': 'Madame Curielaan', 'city': 'Rijswijk', 'country': 'Nederland'}
        self._postcode = '2289CA'
        self._locadress = None
        self._latitude: float = 0
        self._longitude: float = 0
    
    def __str__(self) -> str:
        return f"({self._postcode})"

    def adress(self):
        # calling the Nominatim tool and create Nominatim class
        loc = Nominatim(user_agent="Geopy Library")

        # entering the location name
        getLoc = loc.geocode(self._adres)

        self._locadress = getLoc.address
        self._latitude = getLoc.latitude
        self._longitude = getLoc.longitude

        #Coordinates object aanmaken
        coordinate = Coordinates(self._latitude, self._longitude)

        return coordinate.coordinates
    
    @property
    def latitude(self):
        return self._latitude
    
    @property
    def longitude(self):
        return self._longitude
    

    
