from enum import Enum, auto
from source.structures import Coordinates, ID
from source.constants import Constants
from geopy.geocoders import Nominatim
import pandas as pd
from geopy.exc import GeocoderTimedOut

class Location_type(Enum):
    HUB = auto()
    ZIEKENHUIS = auto()

class Location:
    def __init__(self, name: str, type: Location_type, postcode = "", **kwargs) -> None:
        self._name = name
        self._type = type
        if postcode == "": 
            self._postcode = self.get_postcode()
        else:
            self._postcode = postcode
        self._coordinates = self.postcode_to_coordinates()
        self._id = ID()
    
    def __str__(self) -> str:
        return f"{self._name} ({self._coordinates})"
    
    def get_postcode(self) -> str:
        """
        Haal de postcode van de locatie op

        Returns:
            postcode (str): De postcode van de locatie
        """
        # csv inladen
        csv_locations_data_path = Constants.LOCATIONS_PATH / 'locations_data.csv'
        csv_locations = pd.read_csv(csv_locations_data_path, sep = ';', header = 0, keep_default_na=False)

        # controleer of gevraagde naam voorkomt in de dataset
        if self._name not in set(csv_locations["Naam"].values):
            raise Exception("Deze locatie is niet bekend.")

        # namen van ziekenhuizen als index plaatsen
        csv_locations.set_index('Naam', inplace=True) 
        postcode = csv_locations["Locatie_Postcode"][self._name]
        
        # controleren of er een postcode bij de locatie is opgeslagen
        if postcode == "":
            raise Exception("Van deze locatie is geen postcode bekend.")

        return postcode
    
    def postcode_to_coordinates(self) -> Coordinates:
        """
        Genereer een Coordinates object aan de hand van een postcode

        Returns:
            coordinate (Coordinates): Een Coordinates object met de latitude en longitude
        """
        # calling the Nominatim tool and create Nominatim class
        loc = Nominatim(user_agent="Geopy Library")

        attempt = False
        count = 0
        while attempt == False and count < 5:
            print('attempt', count)
            attempt = True
            try:
                getLoc = loc.geocode(self._postcode)
                print('gelukt?')
            except GeocoderTimedOut:
                attempt = False
                count += 1
                print('failed', count)
        
        print('5 tests gedaan')
        # postcode invoeren
        getLoc = loc.geocode(self._postcode)
        
        # controleren of er een locatie met de gegeven postcode is gevonden
        if getLoc is None:
            raise Exception("Deze locatie is niet correct of ligt niet in Nederland.")
        
        if getLoc.address.endswith("Nederland"):
            # Coordinates object aanmaken
            coordinate = Coordinates(getLoc.latitude, getLoc.longitude)
            return coordinate
        else:
            raise Exception("Deze locatie ligt niet in Nederland.")

    @property
    def coordinates(self):
        return self._coordinates
    
    @property
    def name(self):
        return self._name
    
    @property
    def type(self):
        return self._type
    
    @property
    def id(self):
        return self._id
