from pathlib import Path

class Constants:
    """
    Een class die de constante waarden van de simulatie bevat.
    """

    PRIJS_PER_KM = 0.0
    PRIJS_PER_UUR_CHAUFFEUR = 0.0
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
    LOCATIONS_PATH = Path(__file__).resolve().parents[2] / 'locations_data'
