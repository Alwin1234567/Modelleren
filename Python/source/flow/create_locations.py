from source.constants import Constants
from source.locations import Location, Ziekenhuis, Hub
import pandas as pd
from warnings import warn
from source.structures import Status, Timeslot

class Create_locations:
    """
    Een class die de locaties aanmaakt en in een lijst zet.
    """
    
    def __init__(self) -> None:
        self._hubs = []
        self._status = Status.PREPARING
        hub_data, ziekenhuizen_data = self.load_data()
        self.create_hubs(hub_data, ziekenhuizen_data)
        self.status = Status.FINISHED
    
    def load_data():
        """
        Laad de data in van de locaties.
        """
        locations_data = pd.read_csv(Constants.LOCATIONS_PATH / 'locations.csv')
        
        # Zet alle tekst om naar kleine letters
        locations_data = locations_data.applymap(lambda s: s.lower() if type(s) == str else s)
        
        ziekenhuizen_data = locations_data[locations_data['locatie_type'] == 'ziekenhuis']
        hub_data = locations_data[locations_data['locatie_type'] == 'hub']
        
        # Verwijder kolommen die alleen NaN-waarden bevatten in hub_data
        hub_data = hub_data.dropna(axis=1, how='all')
        
        # Controleer of alle waarden in "Hub_Voorkeur" in de "naam" kolom van hub_data staan
        if not ziekenhuizen_data['hub_voorkeur'].isin(hub_data['naam']).all():
            warn("Sommige hubs in 'Hub_Voorkeur' komen niet voor in de database.")
        
        return hub_data, ziekenhuizen_data
    
    def create_hubs(self, hub_data: pd.DataFrame, ziekenhuizen_data: pd.DataFrame) -> None:
        """
        Maak de hubs aan en voeg de ziekenhuizen toe.

        Parameters:
            hub_data (pd.DataFrame): Een DataFrame met de hub data.
            ziekenhuizen_data (pd.DataFrame): Een DataFrame met de ziekenhuis data.
        """
        if self._status != Status.PREPARING:
            raise Exception("Het is niet mogelijk om de hubs aan te maken als de status niet 'PREPARING' is.")
        for _, hub_series in hub_data.iterrows():
            hub = Hub(hub_series['naam'], postcode=hub_series["postcode"])
            self._hubs.append(hub)
            linked_ziekenhuizen: pd.DataFrame = ziekenhuizen_data[ziekenhuizen_data['hub_voorkeur'] == hub_series['naam']]
            for _, ziekenhuis_series in linked_ziekenhuizen.iterrows():
                timeslots = self.get_ziekenhuis_timeslots(ziekenhuis_series)
                vraag, aanbod = self.get_ziekenhuis_vraag_aanbod(ziekenhuis_series)
                ziekenhuis = Ziekenhuis(ziekenhuis_series['naam'], vraag, aanbod, postcode=ziekenhuis_series['postcode'])
                hub.add_ziekenhuis(ziekenhuis)
            hub.finish_creation()
    
    def get_ziekenhuis_timeslots(self, ziekenhuis: pd.Series) -> list[Timeslot]:
        pass

    def get_ziekenhuis_vraag_aanbod(self,ziekenhuis: pd.Series) -> tuple:
        """
        Haal de vraag en het aanbod van een ziekenhuis op.

        Parameters:
            ziekenhuis (pd.Series): Een Series met de ziekenhuis data.
        """
        return [0]*7, [0]*7 # tijdelijke oplossing
        vraag = ziekenhuis['vraag']
        aanbod = ziekenhuis['aanbod']
        return vraag, aanbod
    
    @property
    def hubs(self):
        return self._hubs
    
    @property
    def status(self):
        return self._status
