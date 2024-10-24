from pathlib import Path
from datetime import time

class Constants:
    """
    Een class die de constante waarden van de simulatie bevat.
    """

    PRIJS_PER_KM = 0.0  #bakwagen: 7.2 L/100km, bestelbus: 6.8 L/100km
    PRIJS_PER_UUR_CHAUFFEUR = 0.0 #06:00-20:00 - 22.75, 20:00-00:00 - 29,575, 00:00-06:00 - 34,125
    TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT = 5.0 #5 tot 10 min
    TIJDSDUUR_INLADEN_EN_UITLADEN_INSTRUMENTENSETS = 0.0
    CAPACITEIT_VOERTUIG = 0
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
