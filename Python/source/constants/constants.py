from pathlib import Path
from datetime import time

class Constants:
    """
    Een class die de constante waarden van de simulatie bevat.
    """

    PRIJS_PER_KM = 0.0  #bakwagen: 7.2 L/100km, bestelbus: 6.8 L/100km
    TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT = 5.0 #5 tot 10 min
    TIJDSDUUR_INLADEN_EN_UITLADEN_INSTRUMENTENSETS = 0.0
    TIJDSDUUR_SCHOONMAAK = 6*60
    CAPACITEIT_VOERTUIG = 35
    BRANDSTOFPRIJS = 1.80
    PRIJS_PER_KM_BAKWAGEN = (BRANDSTOFPRIJS * 7.2) / 100 # bakwagen: 7.2 L/100km
    PRIJS_PER_KM_BESTELBUS = (BRANDSTOFPRIJS * 6.8) / 100  # bestelbus: 6.8 L/100km
    TIJDSDUUR_INLADEN_EN_UITLADEN_BAKWAGEN = 0.5
    TIJDSDUUR_INLADEN_EN_UITLADEN_BESTELBUS = 0.3
    CAPACITEIT_BAKWAGEN = 9 # karren
    CAPACITEIT_BESTELBUS = 22 # bakken
    TIJDSDUUR_SCHOONMAAK = 4 * 60
    WACHTTIJD_TUSSEN_ROUTES = 30 # half uur wachten tussen twee routes voor opvangen vertraging voorgaande routes

    CAPACITEIT_KAR = 18 # sets per kar
    CAPACITEIT_BAK = 4 # sets per bak
    BAKKEN_PER_KAR = 8 # aantal bakken die op de plek van één kar in een bakwagen passen
    
    MAPS_URL = "http://localhost:8989/route"
    MAPS_PARAMS = {
        'profile': 'car',
        'locale': 'en',
        'calc_points': 'false'
    }
    STARTUP_WAIT_TIME = 5
    CACHE_PATH = Path(__file__).resolve().parents[2] / 'cache'
    GRAPHHOPPER_PATH = Path(__file__).resolve().parents[2] / 'graphhopper'
    LOCATIONS_PATH = Path(__file__).resolve().parents[2] / 'locations_data'
    
    PRIJS_PER_UUR_CHAUFFEUR = 22.75
    EXTRA_AVOND = 0.3
    EXTRA_NACHT = 0.5
    TIJD_DAG = (time(6, 0), time(20, 0))
    TIJD_AVOND = (time(20, 0), time(0, 0))
    TIJD_NACHT = (time(0, 0), time(6, 0))

    EXCEL_BESTAND_NAAM = "data_locaties.xlsx"
    EXCEL_ZIEKENHUIZEN_SHEET = "Algemene_ziekenhuisgegevens"
    EXCEL_HUB_SHEET = "Algemene_hubgegevens"
    EXCEL_TAKEN_SHEET = "Tijdvakken_en_vraag"
