from datetime import datetime, timedelta, time
from source.constants import Constants
from typing import Tuple
from .tijdslot import Tijdslot

class Cost:
    
    @staticmethod
    def calculate_cost_time(start_time: time, duration: float) -> float:
        """
        Calculate the cost of a shift based on the start time and duration in minutes.
        
        Parameters:
            start_time (time): The start time of the shift.
            duration (float): The duration of the shift in minutes.
        
        Returns:
            float: The total cost of the shift.
        """
        def is_within_period(time_period: Tuple[time], check_time: time) -> bool:
            start, end = time_period
            if start <= end:
                return start <= check_time < end
            else:
                return start <= check_time or check_time < end
        
        def get_next_period(current_period: str) -> str:
            if current_period == "dag":
                return "avond"
            elif current_period == "avond":
                return "nacht"
            else:
                return "dag"
        
        def get_period(start: time) -> str:
            """
            Get the period of the day based on the start time.

            Parameters:
                start (time): The start time.

            Returns:
                str: The period of the day ('dag', 'avond', 'nacht').
            """
            if is_within_period(Constants.TIJD_DAG, start):
                return "dag"
            elif is_within_period(Constants.TIJD_AVOND, start):
                return "avond"
            elif is_within_period(Constants.TIJD_NACHT, start):
                return "nacht"
            else:
                raise ValueError("Invalid start time")

        def calculate_cost(duration: timedelta, period: str) -> float:
            day_cost = duration.total_seconds() / 3600.0 * Constants.PRIJS_PER_UUR_CHAUFFEUR
            if period == "dag":
                return day_cost
            elif period == "avond":
                return day_cost * (1 + Constants.EXTRA_AVOND)
            else:
                return day_cost * (1 + Constants.EXTRA_NACHT)
        
        def get_duration(period: str, start: time) -> timedelta:
            """
            Get the duration from the given start time to the end of the specified period.

            Parameters:
                period (str): The period ('dag', 'avond', 'nacht').
                start (time): The start time.

            Returns:
                timedelta: The duration from the start time to the end of the period.
            """
            today = datetime.today()
            
            if period == "dag":
                period_end = Constants.TIJD_DAG[1]
            elif period == "avond":
                period_end = Constants.TIJD_AVOND[1]
            elif period == "nacht":
                period_end = Constants.TIJD_NACHT[1]
            else:
                raise ValueError("Invalid period")

            start_dt = datetime.combine(today, start)
            period_end_dt = datetime.combine(today, period_end)

            # Handle periods that go through midnight
            if period_end < start:
                period_end_dt += timedelta(days=1)

            return period_end_dt - start_dt
        
        current_time = start_time

        total_cost = 0.0
        
        remaining_duration = timedelta(minutes=duration)
        
        while remaining_duration > timedelta():
            period = get_period(current_time)
            time_in_period = min(get_duration(period, current_time), remaining_duration)
            total_cost += calculate_cost(time_in_period, period)
            remaining_duration = max(remaining_duration - time_in_period, timedelta())
            current_time = (datetime.combine(datetime.today(), current_time) + time_in_period).time()
        
        return total_cost

    @staticmethod
    def calculate_cost_distance(distance_km: float) -> float:
        """
        Calculate the cost based on the distance given.
        
        Parameters:
            distance_km (float): The distance in kilometers.
        
        Returns:
            float: The total cost based on the distance.
        """
        return distance_km * Constants.PRIJS_PER_KM
