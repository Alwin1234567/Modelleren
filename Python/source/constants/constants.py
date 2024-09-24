class Constants:
    """
    Een class die de constante waarden van de simulatie bevat.
    """

    def __init__(self):
        self._prijs_per_km = 0.0
        self._prijs_per_uur_chauffeur = 0.0
        self._tijdsduur_inladen_en_uitladen_plat = 0.0
        self._tijdsduur_inladen_en_uitladen_instrumentensets = 0.0
        self._capaciteit_voertuig = 0

    @property
    def prijs_per_km(self):
        """
        De prijs per gereden kilometer van de auto in euro's.
        """
        return self._prijs_per_km

    @property
    def prijs_per_uur_chauffeur(self):
        """
        uurloon van de chauffeur in euro's.
        """
        return self._prijs_per_uur_chauffeur

    @property
    def tijdsduur_inladen_en_uitladen_plat(self):
        """
        De vaste tijd die altijd nodig is als het voertuig stopt om in- of uit te laden in minuten.
        """
        return self._tijdsduur_inladen_en_uitladen_plat

    @property
    def tijdsduur_inladen_en_uitladen_instrumentensets(self):
        """
        De tijd die nodig is voor het in- en uitladen van één instrumentenset in minuten.
        """
        return self._tijdsduur_inladen_en_uitladen_instrumentensets

    @property
    def capaciteit_voertuig(self):
        """
        De capaciteit van het voertuig in grootte van de instrumentensets.
        De standaard grootte van een instrumentenset is 1000.
        """
        return self._capaciteit_voertuig

    def tijdsduur_inladen_en_uitladen(self, aantal_instrumentensets: int):
        """
        Bereken de tijd die nodig is voor het in- en uitladen van een aantal instrumentensets.

        Parameters:
            aantal_instrumentensets (int): Het aantal instrumentensets dat in- en uitgeladen moet worden.

        Returns:
            float: De tijd die nodig is voor het in- en uitladen van de instrumentensets.
        """
        return self._tijdsduur_inladen_en_uitladen_plat + (aantal_instrumentensets * self._tijdsduur_inladen_en_uitladen_instrumentensets)

    def rijkosten(self, afstand: float, tijd: float):
        """
        Bereken de rijkosten voor een rit.
        
        Parameters:
            afstand (float): De afstand van de rit in kilometers.
            tijd (float): De tijd van de rit in minuten.

        Returns:
            float: De rijkosten voor de rit.
        """
        return afstand * self._prijs_per_km + tijd * self._prijs_per_uur_chauffeur
