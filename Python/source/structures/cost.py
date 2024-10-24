from datetime import datetime, timedelta, time
from source.constants import Constants

class Cost:
    
    @staticmethod
    def calculate_cost_time(start_time: time, duration_minutes: float) -> float:
        """
        Calculate the cost of a shift based on the start time and duration in minutes.
        
        Parameters:
            start_time (time): The start time of the shift.
            duration_minutes (float): The duration of the shift in minutes.
        
        Returns:
            float: The total cost of the shift.
        """
        total_cost = 0.0
        
        # Convert start time to datetime for easier manipulation
        start_dt = datetime.combine(datetime.today(), start_time)
        duration = timedelta(minutes=duration_minutes)
        end_dt = start_dt + duration
        
        current_time = start_dt
        
        while current_time < end_dt:
            if Constants.TIJD_DAG[0] <= current_time.time() < Constants.TIJD_DAG[1]:
                next_period = min(end_dt, datetime.combine(current_time.date(), Constants.TIJD_DAG[1]))
                multiplier = 1.0  # Day shift has no extra cost
            elif Constants.TIJD_AVOND[0] <= current_time.time() or current_time.time() < Constants.TIJD_AVOND[1]:
                next_period = min(end_dt, datetime.combine(current_time.date(), Constants.TIJD_AVOND[1]))
                multiplier = 1.0 + Constants.EXTRA_AVOND
            else:
                next_period = min(end_dt, datetime.combine(current_time.date(), Constants.TIJD_NACHT[1]))
                multiplier = 1.0 + Constants.EXTRA_NACHT
            
            # Calculate the duration in hours
            duration_hours = (next_period - current_time).total_seconds() / 3600.0
            total_cost += duration_hours * Constants.PRIJS_PER_UUR_CHAUFFEUR * multiplier
            
            current_time = next_period
        
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
