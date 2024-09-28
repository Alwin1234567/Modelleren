from geopy.geocoders import Nominatim
from .coordinates import Coordinates

class LocationToCoordinates:
    def __init__(self, postcode) -> None:
        self._adres = {'street': 'Madame Curielaan', 'city': 'Rijswijk', 'country': 'Nederland'} #{'street': 'leidsestraatweg', 'country': 'Nederland'} 
        self._postcode = postcode
        self._locadress = None
        self._latitude: float = 0
        self._longitude: float = 0
    
    def lat_lon_from_adress(self):
        """
        Genereer een Coordinates object aan de hand van een adres
        """

        # calling the Nominatim tool and create Nominatim class
        loc = Nominatim(user_agent="Geopy Library")

        # entering the location name
        getLoc = loc.geocode(self._adres)

        #Dit kan uiteindelijk weggelaten worden
        self._locadress = getLoc.address
        self._latitude = getLoc.latitude
        self._longitude = getLoc.longitude

        #Coordinates object aanmaken
        coordinate = Coordinates(getLoc.latitude, getLoc.longitude)

        return coordinate.coordinates
    
    def lat_lon_from_postcode(self):
        """
        Genereer een Coordinates object aan de hand van een postcode
        """

        # calling the Nominatim tool and create Nominatim class
        loc = Nominatim(user_agent="Geopy Library")

        # entering the location name
        getLoc = loc.geocode(self._postcode)
        
        #controleren of er een locatie met de gegeven postcode is gevonden
        if getLoc is None:
            print("Postcode is niet correct of ligt niet in Nederland.")
            return None
        
        #Dit kan uiteindelijk weggelaten worden
        self._locadress = getLoc.address
        self._latitude = getLoc.latitude
        self._longitude = getLoc.longitude
        
        #controleren of de gevonden locatie in Nederland ligt
        if self._locadress.endswith("Nederland"):
            #Coordinates object aanmaken
            coordinate = Coordinates(getLoc.latitude, getLoc.longitude)
            return coordinate.coordinates
        else:
            print("Postcode ligt niet in Nederland.")
            return None
    
    @property
    def latitude(self):
        return self._latitude
    
    @property
    def longitude(self):
        return self._longitude
    

    
