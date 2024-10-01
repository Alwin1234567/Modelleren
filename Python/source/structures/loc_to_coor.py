from geopy.geocoders import Nominatim
from .coordinates import Coordinates
import pandas

class LocationToCoordinates:
    def __init__(self, postcode: str) -> None:
        self._postcode = postcode
        self._locadress = None
        self._latitude: float = 0
        self._longitude: float = 0
    
    def lat_lon_from_postcode(self) -> Coordinates:
        """
        Genereer een Coordinates object aan de hand van een postcode

        Returns:
            coordinate (Coordinates): Een Coordinates object met de latitude en longitude
        """

        # calling the Nominatim tool and create Nominatim class
        loc = Nominatim(user_agent="Geopy Library")

        # entering the location name
        getLoc = loc.geocode(self._postcode)
        
        #controleren of er een locatie met de gegeven postcode is gevonden
        if getLoc is None:
            print("Postcode is niet correct of ligt niet in Nederland.")
            return None #aanpassen afhankelijk van foutafhandeling
        
        #Dit kan uiteindelijk weggelaten worden
        self._locadress = getLoc.address
        self._latitude = getLoc.latitude
        self._longitude = getLoc.longitude
        
        #controleren of de gevonden locatie in Nederland ligt
        if self._locadress.endswith("Nederland"):
            #Coordinates object aanmaken
            coordinate = Coordinates(getLoc.latitude, getLoc.longitude)
            return coordinate
        else:
            print("Postcode ligt niet in Nederland.")
            return None #aanpassen afhankelijk van foutafhandeling
    
    @property
    def latitude(self):
        return self._latitude
    
    @property
    def longitude(self):
        return self._longitude

class ReadLocation:
    def __init__(self, location: str) -> None:
        self._location = location.lower()
        self._path = 'source/structures/locations_adresses.csv' #path-object van maken met pathlib
        self._postcode: str = None
    
    def postcode(self) -> str:
        """
        Vindt de postcode van een locatie aan de hand van de locatienaam.
        """
        
        #csv inladen
        csv_locations = pandas.read_csv(self._path, sep = ';', header = 0, keep_default_na=False)

        #verwijder de substring '\t' die soms achter de naam komt en alle namen omzetten naar kleine letters
        csv_locations["Naam"] = csv_locations["Naam"].str.replace('\t', '').str.lower()

        #controleer of gevraagde naam voorkomt in de dataset
        if self._location not in csv_locations["Naam"].values:
            print(f"De locatie met naam {self._location} is niet bekend.")
            return None #aanpassen afhankelijk van foutafhandeling

        #namen van ziekenhuizen als index plaatsen
        csv_locations.set_index('Naam', inplace=True) 

        #postcode nemen op index met juiste locatienaam
        self._postcode = csv_locations["Locatie_Postcode"][self._location]
        
        #controleren of er een postcode bij de locatie is opgeslagen
        if self._postcode != "":
            return self._postcode
        else:
            print("geen postcode van deze locatie opgeslagen")
            return None #aanpassen afhankelijk van foutafhandeling
