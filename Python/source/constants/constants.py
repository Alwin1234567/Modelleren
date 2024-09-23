class Constants:

    def __init__(self):
        self._prijs_per_km = 0.0
        self._prijs_per_uur_chauffeur = 0.0
        self._tijdsduur_inladen_en_uitladen_plat = 0.0
        self._tijdsduur_inladen_en_uitladen_instrumentensets = 0.0
        self._capaciteit_voertuig = 0

    @property
    def prijs_per_km(self):
        return self._prijs_per_km

    @property
    def prijs_per_uur_chauffeur(self):
        return self._prijs_per_uur_chauffeur

    @property
    def tijdsduur_inladen_en_uitladen_plat(self):
        return self._tijdsduur_inladen_en_uitladen_plat

    @property
    def tijdsduur_inladen_en_uitladen_instrumentensets(self):
        return self._tijdsduur_inladen_en_uitladen_instrumentensets

    @property
    def capaciteit_voertuig(self):
        return self._capaciteit_voertuig

    def tijdsduur_inladen_en_uitladen(self, aantal_instrumentensets):
        return self._tijdsduur_inladen_en_uitladen_plat + (aantal_instrumentensets * self._tijdsduur_inladen_en_uitladen_instrumentensets)
