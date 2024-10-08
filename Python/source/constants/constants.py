from pathlib import Path
from datetime import time

class Constants:
    """
    Een class die de constante waarden van de simulatie bevat.
    """

    PRIJS_PER_KM = 0.0
    TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT = 0.0
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
    
    PRIJS_PER_UUR_CHAUFFEUR = 22.75
    EXTRA_AVOND = 0.3
    EXTRA_NACHT = 0.5
    TIJD_DAG = (time(6, 0), time(20, 0))
    TIJD_AVOND = (time(20, 0), time(0, 0))
    TIJD_NACHT = (time(0, 0), time(6, 0))
