from datetime import time
from source.constants import Constants

class Distance_time:
    """
    Een class om de afstand en tijd tussen twee locaties te beheren.
    """

    def __init__(self, distance: float, time: float) -> None:
        """
        Initialiseer een nieuwe instantie van de Distance_time klasse.

        Parameters:
            distance (float): De afstand tussen twee locaties in kilometers.
            time (float): De tijd tussen twee locaties in minuten.
        """
        self._distance = distance
        self._time = time
    
    def cost(self, start_time: time) -> float:
        """
        Bereken de kosten van de afstand en tijd.

        Parameters:
            overtime (float): Percentage van de tijd dat in de nacht valt.

        Returns:
            float: De kosten van de afstand en tijd.
        """
        pass

    @property
    def distance(self) -> float:
        """
        Haal de afstand op.

        Returns:
            float: De afstand tussen twee locaties in kilometers.
        """
        return self._distance

    @property
    def time(self) -> float:
        """
        Haal de tijd op.

        Returns:
            float: De tijd tussen twee locaties in minuten.
        """
        return self._time
