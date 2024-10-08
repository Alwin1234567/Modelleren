from enum import Enum, auto
from source.structures import Coordinates, ID
from source.constants import Constants
from geopy.geocoders import Nominatim
import pandas as pd

class Location_type(Enum):
    HUB = auto()
    ZIEKENHUIS = auto()

class Location:
    def __init__(self, name: str, type: Location_type) -> None:
        self._name = name
        self._type = type
        self._coordinates = self.name_to_coordinates()
        self._id = ID()
    
    def __str__(self) -> str:
        return f"{self._name} ({self._coordinates})"
    
    def name_to_coordinates(self) -> Coordinates:
        """
        Genereer een Coordinates object aan de hand van een klinieknaam

        Returns:
            coordinate (Coordinates): Een Coordinates object met de latitude en longitude
        """
        # csv inladen
        csv_locations_data_path = Constants.LOCATIONS_PATH / 'locations_data.csv'
        csv_locations = pd.read_csv(csv_locations_data_path, sep = ';', header = 0, keep_default_na=False)

        # controleer of gevraagde naam voorkomt in de dataset
        if self._name not in set(csv_locations["Naam"].values):
            raise Exception("Deze locatie is niet bekend.")

        # namen van ziekenhuizen als index plaatsen
        csv_locations.set_index('Naam', inplace=True) 
        self._postcode = csv_locations["Locatie_Postcode"][self._name]
        
        # controleren of er een postcode bij de locatie is opgeslagen
        if self._postcode == "":
            raise Exception("Van deze locatie is geen postcode bekend.")

        # calling the Nominatim tool and create Nominatim class
        loc = Nominatim(user_agent="Geopy Library")

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
