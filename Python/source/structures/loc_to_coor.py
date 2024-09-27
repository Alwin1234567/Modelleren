from geopy.geocoders import Nominatim

class LocationToCoordinates:
    def __init__(self) -> None:
        self._adres = {'street': 'Madame Curielaan', 'city': 'Rijswijk', 'county': '', 'state': '', 'country': 'Netherlands'}
        self._postcode = '2289CA'
    
    def __str__(self) -> str:
        return f"({self._postcode})"

    def lat(self):
        # calling the Nominatim tool and create Nominatim class
        loc = Nominatim(user_agent="Geopy Library")

        # entering the location name
        getLoc = loc.geocode("İzmir")

        adress = getLoc.address
        latitude = getLoc.latitude
        longitude = getLoc.longitude

        return adress
    
    @property
    def coordinates(self):
        return (self.lat, self.lon)
    
