from pathlib import Path
from datetime import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source.structures import Auto_type, Bak_kar_voorkeur

class Constants:
    """
    Een class die de constante waarden van de simulatie bevat.
    """

    TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT = 5.0 #5 tot 10 min
    TIJDSDUUR_SCHOONMAAK = 4 * 60
    WACHTTIJD_TUSSEN_ROUTES = 30 # half uur wachten tussen twee routes voor opvangen vertraging voorgaande routes
    BAKKEN_PER_KAR = 8 # aantal bakken die op de plek van één kar in een bakwagen passen

    @staticmethod
    def prijs_per_km(auto_type: "Auto_type") -> float:
        BRANDSTOFPRIJS = 1.80
        if str(auto_type) == "Auto_type.BAKWAGEN":
            # 7.2 L/100 km
            return (BRANDSTOFPRIJS * 7.2) / 100
        elif str(auto_type) == "Auto_type.BESTELBUS":
            # 6.8 L/100 km
            return (BRANDSTOFPRIJS * 6.8) / 100
    
    @staticmethod
    def capaciteit_auto(auto_type: "Auto_type") -> int:
        if str(auto_type) == "Auto_type.BAKWAGEN":
            # 9 karren per bakwagen
            return 9
        elif str(auto_type) == "Auto_type.BESTELBUS":
            # 22 bakken per bestelbus
            return 22
    
    @staticmethod
    def capaciteit_bak_kar(bak_kar_voorkeur: "Bak_kar_voorkeur") -> int:
        if str(bak_kar_voorkeur) == "Bak_kar_voorkeur.KAR":
            # 18 sets per kar
            return 18
        elif str(bak_kar_voorkeur) == "Bak_kar_voorkeur.BAK":
            # 4 sets per bak
            return 4

    @staticmethod
    def tijdsduur_in_en_uitladen(bak_kar_voorkeur: "Bak_kar_voorkeur") -> float:
        if str(bak_kar_voorkeur) == "Bak_kar_voorkeur.KAR":
            return 0.5
        elif str(bak_kar_voorkeur) == "Bak_kar_voorkeur.BAK":
            return 0.3

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
