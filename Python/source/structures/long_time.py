from typing import Union, Tuple
from datetime import time, timedelta
from warnings import warn

class Long_time:
    """
    Een variatie op de Tijdslot class die tijden tot 7200 minuten (5 dagen) kan representeren.
    """

    def __init__(self, tijd: Union[time, float, int], dag: int = 0) -> None:
        """
        Creëer een nieuw tijdslot.
        """
        self._tijd, self._dag = self._tijd_interpreteren(tijd, dag)
        if self._dag > 5:
            warn("De dag van de long_time is groter dan 5.", RuntimeWarning)
    
    def _tijd_interpreteren(self, tijd: Union[time, float, int], dag: int = 0) -> Tuple[time, int]:
        """
        Zet tijd om naar time en dag.

        Parameters:
            tijd (Union[time, float]): De tijd die omgezet moet worden.
            dag (int): De dag die meegegeven wordt. Standaard is 0.

        Returns:
            Tuple[time, int]: De tijd en de dag.
        """
        if isinstance(tijd, int):
            tijd = float(tijd)
        if isinstance(tijd, time):
            return tijd, dag
        if isinstance(tijd, float):
            seconden = int((tijd % 1) * 60)
            minuten = int(tijd % 60)
            uren = int((tijd // 60) % 24)
            tempdag = int(tijd // 1440)  # 1440 minutes in a day
            if tempdag > 0:
                if dag > 0:
                    warn("er is beide een dag en een float groter dan 1440 meegegeven, de dag wordt genegeerd.", RuntimeWarning)
                dag = tempdag
            return time(uren, minuten, seconden), dag
        raise ValueError("De tijd moet een time of float zijn.")
    
    def __float__(self) -> float:
        """
        Zet de long_time om naar een float.

        Returns:
            float: De tijd in minuten.
        """
        dagminuten = self._dag * 1440
        urenminuten = self._tijd.hour * 60
        minuten = self._tijd.minute
        secondenminuten = self._tijd.second / 60
        return float(dagminuten + urenminuten + minuten + secondenminuten)

    def __gt__(self, other: 'Long_time') -> bool:
        """
        Vergelijk twee Long_time objecten.

        Parameters:
            other (Long_time): Het andere Long_time object.

        Returns:
            bool: True als self groter is dan other, anders False.
        """
        return float(self) > float(other)
    
    def __ge__(self, other: 'Long_time') -> bool:
        """
        Vergelijk twee Long_time objecten.

        Parameters:
            other (Long_time): Het andere Long_time object.

        Returns:
            bool: True als self groter of gelijk is aan other, anders False.
        """
        return float(self) >= float(other)
    
    def __eq__(self, other: 'Long_time') -> bool:
        """
        Vergelijk twee Long_time objecten op gelijkheid.

        Parameters:
            other (Long_time): Het andere Long_time object.

        Returns:
            bool: True als self gelijk is aan other, anders False.
        """
        return float(self) == float(other)
    
    def __lt__(self, other: 'Long_time') -> bool:
        """
        Vergelijk twee Long_time objecten.

        Parameters:
            other (Long_time): Het andere Long_time object.

        Returns:
            bool: True als self kleiner is dan other, anders False.
        """
        return float(self) < float(other)
    
    def __le__(self, other: 'Long_time') -> bool:
        """
        Vergelijk twee Long_time objecten.

        Parameters:
            other (Long_time): Het andere Long_time object.

        Returns:
            bool: True als self kleiner of gelijk is aan other, anders False.
        """
        return float(self) <= float(other)
    
    def __add__(self, other: Union[float, int, time, "Long_time"]) -> 'Long_time':
        """
        Voeg een float of time toe aan de Long_time.

        Parameters:
            other (Union[float, int, time, Long_time]): De tijd die toegevoegd moet worden.

        Returns:
            Long_time: Een nieuwe Long_time met de toegevoegde tijd.
        """
        if isinstance(other, int):
            other = float(other)
        if isinstance(other, float):
            total_minutes = float(self) + other
        elif isinstance(other, time):
            total_minutes = float(self) + other.hour * 60 + other.minute
        elif isinstance(other, Long_time):
            total_minutes = float(self) + float(other)
        else:
            raise TypeError("De tijd moet een float, int, time of Long_time zijn.")
        
        return Long_time(total_minutes)
    
    def __sub__(self, other: Union[float, int, time, "Long_time"]) -> 'Long_time':
        """
        Trek een float of time af van de Long_time.

        Parameters:
            other (Union[float, int, time, Long_time]): De tijd die afgetrokken moet worden.

        Returns:
            Long_time: Een nieuwe Long_time met de afgetrokken tijd.
        """
        if isinstance(other, int):
            other = float(other)
        if isinstance(other, float):
            total_minutes = float(self) - other
        elif isinstance(other, time):
            total_minutes = float(self) - (other.hour * 60 + other.minute)
        elif isinstance(other, Long_time):
            total_minutes = float(self) - float(other)
        else:
            raise TypeError("De tijd moet een float, int, time of Long_time zijn.")
        
        if total_minutes < 0:
            warn("Het resultaat is negatief.", RuntimeWarning)
        
        return Long_time(total_minutes)
    
    def difference(self, other: 'Long_time') -> float:
        """
        Bereken het tijdverschil tussen twee Long_time objecten.

        Parameters:
            other (Long_time): Het andere Long_time object.

        Returns:
            float: Het verschil in minuten.
        """
        return abs(float(self) - float(other))
    
    @property
    def tijd(self) -> time:
        """
        De tijd van de long_time.
        """
        return self._tijd
    
    @property
    def dag(self) -> int:
        """
        De dag van de long_time.
        """
        return self._dag
