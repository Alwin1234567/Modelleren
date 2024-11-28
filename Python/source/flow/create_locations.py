from source.constants import Constants
from source.locations import Ziekenhuis, Hub
import pandas as pd
from warnings import warn
from source.structures import Status, Taak, Long_time, Tijdslot, Maps, Bak_kar_voorkeur
from datetime import time

class Create_locations:
    """
    Een class die de locaties aanmaakt en in een lijst zet.
    """
    
    def __init__(self) -> None:
        self._hubs: list[Hub] = []
        self._status = Status.PREPARING
        self._ziekenhuizen: dict[str, Ziekenhuis] = {}
        hub_data, ziekenhuizen_data = self.load_data()
        self.create_hubs(hub_data, ziekenhuizen_data)
        Maps.disable_maps()
        self.add_taken()
        self._finish_creation()
        self._status = Status.FINISHED
    
    def load_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Laad de data in van de locaties.

        Returns:
            tuple[pd.DataFrame, pd.DataFrame]: Een tuple met twee DataFrames. De eerste DataFrame bevat de hub data en de tweede DataFrame bevat de ziekenhuis data.
        """
        ziekenhuizen_data = pd.read_excel(self.excel_path, sheet_name=Constants.EXCEL_ZIEKENHUIZEN_SHEET)
        hub_data = pd.read_excel(self.excel_path, sheet_name=Constants.EXCEL_HUB_SHEET)

        # Verwijder rijen met NaN waarden
        ziekenhuizen_data = self.remove_na_rows(ziekenhuizen_data)
        hub_data = self.remove_na_rows(hub_data)
        
        # # Zet alle tekst om naar kleine letters
        # locations_data = locations_data.applymap(lambda s: s.lower() if type(s) == str else s)
        
        # Controleer of alle waarden in "Hub_Voorkeur" in de "Naam" kolom van hub_data staan
        if not ziekenhuizen_data['Hub_Voorkeur'].isin(hub_data['Naam']).all():
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
            try:
                hub = Hub(hub_series['Naam'], postcode=hub_series["Locatie_Postcode"])
            except ValueError as e:
                if str(e) == "Deze locatie is niet correct of ligt niet in Nederland.":
                    warn(f"Warning: {e} for hub {hub_series['Naam']}. Continuing with the next hub.", RuntimeWarning)
                    continue
                else:
                    raise e
            self._hubs.append(hub)
            linked_ziekenhuizen: pd.DataFrame = ziekenhuizen_data[ziekenhuizen_data['Hub_Voorkeur'] == hub_series['Naam']]
            for _, ziekenhuis_series in linked_ziekenhuizen.iterrows():
                try:
                    if ziekenhuis_series['Kar_Bak_Voorkeur'] == 'bak':
                        ziekenhuis = Ziekenhuis(ziekenhuis_series['Naam'], Bak_kar_voorkeur.BAK, postcode=ziekenhuis_series['Locatie_Postcode'])
                    else:
                        ziekenhuis = Ziekenhuis(ziekenhuis_series['Naam'], Bak_kar_voorkeur.KAR, postcode=ziekenhuis_series['Locatie_Postcode'])
                except ValueError as e:
                    if str(e) == "Deze locatie is niet correct of ligt niet in Nederland.":
                        warn(f"Warning: {e} for ziekenhuis {ziekenhuis_series['Naam']}. Continuing with the next ziekenhuis.", RuntimeWarning)
                        continue
                    else:
                        raise e
                hub.add_ziekenhuis(ziekenhuis)
                self._ziekenhuizen[ziekenhuis.name] = ziekenhuis

    def remove_na_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Verwijder alle rijen met NaN waarden uit een DataFrame.

        Parameters:
            df (pd.DataFrame): De DataFrame waaruit de NaN waarden moeten worden verwijderd.

        Returns:
            pd.DataFrame: De DataFrame zonder NaN waarden.
        """
        initial_row_count = len(df)
        df = df.dropna()
        final_row_count = len(df)
        if initial_row_count > final_row_count:
            warn(f"{initial_row_count - final_row_count} rows with NaN values were removed.", RuntimeWarning)
        return df
        
    def add_taken(self):
        """
        Voeg de taken toe aan de ziekenhuizen.
        """
        df_taken = pd.read_excel(self.excel_path, sheet_name=Constants.EXCEL_TAKEN_SHEET)
        df_taken = self.remove_na_rows(df_taken)

        for hub in self.hubs:
            for ziekenhuis in hub.ziekenhuizen:
                df_ziekenhuis_taken = df_taken[df_taken["Naam"] == ziekenhuis.name]
                if df_ziekenhuis_taken.empty:
                    continue
                for _, df_ziekenhuis_taak in df_ziekenhuis_taken.iterrows():
                    ziekenhuis_taken = self.parse_taak(df_ziekenhuis_taak)
                    for taak in ziekenhuis_taken:
                        ziekenhuis.add_taak(taak)
    
    def parse_taak(self, df_ziekenhuis_taak: pd.Series) -> list[Taak]:
        taken = []
        days = ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag']
        ziekenhuis = self._ziekenhuizen[df_ziekenhuis_taak['Naam']]
        hoeveelheid_sets = df_ziekenhuis_taak['hoeveelheid (sets)']

        for day in days:
            if df_ziekenhuis_taak[day] == 'ja':
                day_index = days.index(day)
                ophalen_start = Long_time(df_ziekenhuis_taak['begin tijdvak ophalen'], day_index)
                ophalen_end = Long_time(df_ziekenhuis_taak['eind tijdvak ophalen'], day_index)

                if ophalen_end < ophalen_start and ophalen_end.time == time(0, 0):
                    ophalen_end.day = (ophalen_end.day + 1)
                
                if ophalen_end < ophalen_start:
                    warn(f"Eind tijd voor ophalen is voor begin tijd voor ziekenhuis {ziekenhuis.name} start: {ophalen_start}, end: {ophalen_end}", RuntimeWarning)
                    continue
                # Calculate retour times based on the duration after the begin tijdvak
                retour_start_duration = df_ziekenhuis_taak['retour vroegst na begin ophaaltijdvak'] * 60  # Convert hours to minutes
                retour_end_duration = df_ziekenhuis_taak['retour binnen (uur) na begin ophaaltijdvak'] * 60  # Convert hours to minutes
                
                retour_start: Long_time = ophalen_start + retour_start_duration
                retour_end: Long_time = ophalen_start + retour_end_duration
                if retour_start.day > 6 and retour_start.day > 6:
                    retour_start.day = retour_start.day % 7
                    retour_end.day = retour_end.day % 7
                    if retour_end < retour_start:
                        retour_start.day = 0
                        if retour_end < retour_start:
                            retour_start = Long_time(0)
                elif retour_end.day > 6:
                    retour_end.day = retour_end.day % 7
                    retour_start = Long_time(0)

                # Adjust for vrijdag to maandag transition
                if day == 'vrijdag' and retour_end.dag % 7 > 4:
                    retour_start = Long_time(retour_start.tijd, 0)
                    retour_end = Long_time(retour_end.tijd, 0)
                    if retour_end < retour_start:
                        retour_end.day += 1

                # Create Tijdslot instances
                tijdslot_ophalen = Tijdslot(ophalen_start, ophalen_end)
                tijdslot_brengen = Tijdslot(retour_start, retour_end)

                returntijd = Tijdslot(Long_time(7*24*60), Long_time(7*24*60))
                if retour_start > ophalen_end:
                    returntijd = tijdslot_brengen

                if hoeveelheid_sets <= 0:
                    continue

                # Create Taak instances for ophalen and brengen
                try:
                    taak_ophalen = Taak(tijdslot_ophalen, ziekenhuis, halen=hoeveelheid_sets, returntijd=returntijd)
                    taak_brengen = Taak(tijdslot_brengen, ziekenhuis, brengen=hoeveelheid_sets)
                except ValueError as e:
                    warn(f"Error: {e} for ziekenhuis {ziekenhuis.name}. Continuing with the next taak.", RuntimeWarning)
                    continue

                taken.append(taak_ophalen)
                taken.append(taak_brengen)

        return taken
    
    def _finish_creation(self):
        for hub in self.hubs:
            hub.finish_creation()
    
    @property
    def hubs(self):
        return self._hubs
    
    @property
    def status(self):
        return self._status
    
    @property
    def excel_path(self):
        return Constants.LOCATIONS_PATH / Constants.EXCEL_BESTAND_NAAM
