from .status import Status
from .maps import Maps
from .distance_time import Distance_time
from source.constants import Constants
from pandas import DataFrame
from typing import Dict, List, Tuple, TYPE_CHECKING, Generator, Any
import numpy as np
import requests
from warnings import warn
import pandas as pd
from datetime import time
from tqdm import tqdm

if TYPE_CHECKING:
    from source.locations import Location

class Distances:
    """
    Een class om afstanden tussen locaties te beheren en te berekenen.
    """
    
    def __init__(self) -> None:
        """
        Initialiseer een nieuwe instantie van de Distances klasse.
        """
        self._locations: Dict[str, "Location"] = dict()
        self._distances = DataFrame()
        self._status = Status.PREPARING


    def add_location(self, location: "Location") -> None:
        """
        Voeg een locatie toe aan de set van locaties.

        Parameters:
            location (Location): De locatie die moet worden toegevoegd.
        """
        self._locations[location.name] = location
    
    def generate_distances(self) -> None:
        """
        Genereer de afstanden tussen alle toegevoegde locaties.

        Raises:
            Exception: Als de afstanden al worden berekend of al zijn berekend.
        """
        if self._status == Status.CALCULATING:
            raise Exception("Distances are already being calculated")
        elif self._status == Status.FINISHED:
            raise Exception("Distances are already calculated")
        elif self._status != Status.PREPARING:
            raise Exception("Distances are in an unknown state")
        self._status = Status.CALCULATING

        location_names = self._locations.keys()
        self._distances = DataFrame(index=location_names, columns=location_names)
        self._load_stored_distances()
        missing_distances = self._determine_missing_distances()
        if missing_distances:
            self._determine_distances(missing_distances)
        
        if not self._check_complete():
            raise Exception("Distances are not complete")
        self._store_distances()
        self._status = Status.FINISHED

    def _load_stored_distances(self) -> None:
        """
        Laad opgeslagen afstanden uit een bestand.

        Raises:
            Exception: Als de afstanden niet worden berekend.
        """
        if self._status != Status.CALCULATING:
            raise Exception("Distances are not being calculated")
        
        # Define the CSV file path
        csv_file_path = Constants.CACHE_PATH / 'distance_time.csv'

        # Check if the CSV file exists
        if csv_file_path.exists():
            # Open the CSV file and read the first line to check for a separator
            with open(csv_file_path, 'r') as file:
                first_line = file.readline().strip()
                if first_line.startswith('sep='):
                    separator = first_line.split('=')[1]
                    # Read the CSV file into a DataFrame, skipping the first line
                    stored_df = pd.read_csv(csv_file_path, sep=separator, skiprows=1)
                else:
                    # Default separator if no sep= is found
                    stored_df = pd.read_csv(csv_file_path, sep=';')

            # Iterate over the DataFrame and populate self._distances
            for _, row in stored_df.iterrows():
                from_loc = row['from']
                to_loc = row['to']
                distance = row['distance']
                time = row['time']
                if from_loc in self._distances.index and to_loc in self._distances.columns:
                    self._distances.loc[from_loc, to_loc] = Distance_time(distance, time)
    
    def _store_distances(self) -> None:
        """
        Sla de afstanden op in een csv bestand.
        """
        if self._status != Status.CALCULATING:
            raise Exception("Distances are not being calculated")
        
        # Define the CSV file path
        csv_file_path = Constants.CACHE_PATH / 'distance_time.csv'
        csv_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Read the existing CSV file if it exists
        if csv_file_path.exists():
            with open(csv_file_path, 'r') as file:
                first_line = file.readline().strip()
                if first_line.startswith('sep='):
                    existing_df = pd.read_csv(csv_file_path, sep=';', skiprows=1)
                else:
                    existing_df = pd.read_csv(csv_file_path)
        else:
            existing_df = pd.DataFrame(columns=['from', 'to', 'distance', 'time'])

        # Convert the self._distances matrix to a stacked format using pandas.stack
        stacked_df = self._distances.stack().reset_index()
        stacked_df.columns = ['from', 'to', 'distance_time']

        # Filter out diagonal elements and NaN values
        stacked_df = stacked_df[stacked_df['from'] != stacked_df['to']]
        stacked_df = stacked_df.dropna(subset=['distance_time'])

        # Extract distance and time from the distance_time object
        stacked_df['distance'] = stacked_df['distance_time'].apply(lambda x: x.distance)
        stacked_df['time'] = stacked_df['distance_time'].apply(lambda x: x.time)

        # Drop the distance_time column
        stacked_df = stacked_df.drop(columns=['distance_time'])

        new_df = stacked_df[['from', 'to', 'distance', 'time']]

        # Merge the new data with the existing data
        updated_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=['from', 'to'], keep='last')

        # Write the separator declaration at the start of the file
        with open(csv_file_path, 'w') as f:
            f.write('sep=;\n')

        # Append the DataFrame to the file
        updated_df.to_csv(csv_file_path, mode='a', index=False, sep=';')

    def _determine_missing_distances(self) -> List[Tuple["Location", "Location"]]:
        """
        Bepaal de ontbrekende afstanden tussen locaties.
    
        Returns:
            missing_distances (List[Tuple[Location, Location]]): Een lijst van ontbrekende afstanden.
    
        Raises:
            Exception: Als de afstanden niet worden berekend.
        """
        if self._status != Status.CALCULATING:
            raise Exception("Distances are not being calculated")
        missing_distances = self._distances.isna().stack()
        missing_distances = missing_distances[missing_distances].index.tolist()
        missing_distances = [(self._locations[row], self._locations[col]) for row, col in missing_distances if row != col]
        return missing_distances

    def _determine_distances(self, missing_distances: List[Tuple["Location", "Location"]]) -> None:
        """
        Bepaal de afstanden voor de ontbrekende locaties.

        Parameters:
            missing_distances (List[Tuple[Location, Location]]): Een lijst van ontbrekende afstanden.
        """
        if not Maps.is_enabled():
            Maps.enable_maps()
        
        # Initialize the progress bar
        progress_bar = tqdm(total=len(missing_distances), desc="Determining distances", unit="distance")

        for start, end in missing_distances:
            url = f"{Constants.MAPS_URL}?{start.coordinates.OSRM_str}&{end.coordinates.OSRM_str}&profile={Constants.MAPS_PARAMS['profile']}&locale={Constants.MAPS_PARAMS['locale']}&calc_points={Constants.MAPS_PARAMS['calc_points']}"
            response = requests.get(url)
            result = Distance_time(1e10, 1e10)
            if response.status_code == 200:
                data = response.json()
                if 'paths' in data and len(data['paths']) > 0:
                    path = data['paths'][0]
                    distance: float = path['distance']/1000  # Distance in kilometers
                    time: float = path['time']/1000/60  # Time in minutes
                    result = Distance_time(distance, time)
                else:
                    warn(f"No route found between {start} and {end}")
            self._distances.loc[start.name, end.name] = result
            
            # Update the progress bar
            progress_bar.update(1)
        
        # Close the progress bar
        progress_bar.close()
        
    def _check_complete(self) -> bool:
        """
        Controleer of alle afstanden zijn berekend.

        Returns:
            bool: True als alle afstanden zijn berekend, anders False.
        """
        if self._status != Status.CALCULATING:
            raise Exception("Distances are not being calculated")
        # Mask the diagonal values
        # Convert the DataFrame to a NumPy array
        distances_array = self._distances.isna().to_numpy()

        # Fill the diagonal with a specific value (e.g., 0)
        np.fill_diagonal(distances_array, False)

        # Check for None values excluding the diagonal
        return distances_array.sum() == 0
    
    def get_distance_time(self, start: "Location", end: "Location") -> Distance_time:
        """
        Haal de afstand en tijd op tussen twee locaties.

        Parameters:
            start (Location): De startlocatie.
            end (Location): De eindlocatie.

        Returns:
            Distance_time: De afstand en tijd tussen de locaties.
        """
        if start == end:
            return Distance_time(0, 0)
        return self._distances.loc[start.name, end.name]
    
    def get_distance(self, start: "Location", end: "Location") -> float:
        """
        Haal de afstand op tussen twee locaties.

        Parameters:
            start (Location): De startlocatie.
            end (Location): De eindlocatie.

        Returns:
            float: De afstand tussen de locaties.
        """
        return self.get_distance_time(start, end).distance
    
    def get_time(self, start: "Location", end: "Location") -> float:
        """
        Haal de tijd op tussen twee locaties.

        Parameters:
            start (Location): De startlocatie.
            end (Location): De eindlocatie.

        Returns:
            float: De tijd tussen de locaties.
        """
        return self.get_distance_time(start, end).time
    
    def has_location(self, location: "Location") -> bool:
        """
        Controleer of een locatie aanwezig is in de afstanden.

        Parameters:
            location (Location): De locatie die moet worden gecontroleerd.

        Returns:
            bool: True als de locatie aanwezig is, anders False.
        """
        return location.name in self._locations.keys()
    
    def available_locations(self, location: "Location", skip_locations: list["Location"], start_time: time) -> Generator[Tuple["Location", Distance_time], Any, None]:
        """
        Krijg een generator die locaties en hun afstandstijd ophaalt, gesorteerd op kosten.

        Parameters:
            location (Location): De locatie om vanuit te vertrekken.
            skip_locations (list): Een lijst van locaties om over te slaan.

        Yields:
            tuple: Een tuple met de locatie en de afstandstijd.
        """
        # Filter out the locations to skip
        remaining_locations = [loc for loc in self.locations.values() if loc not in skip_locations and loc != location]

        # Retrieve the distance times for the remaining locations
        distance_times = [(loc, self.get_distance_time(location, loc)) for loc in remaining_locations]

        # Sort the list by cost
        sorted_distance_times = sorted(distance_times, key=lambda x: x[1].cost(start_time))

        # Yield each location and its distance time
        for loc, distance_time in sorted_distance_times:
            yield loc, distance_time

    @property
    def status(self) -> Status:
        """
        Haal de status op.

        Returns:
            Status: De status van de afstanden.
        """
        return self._status
    
    @property
    def locations(self) -> Dict[str, "Location"]:
        """
        Haal de locaties op.

        Returns:
            Set[Location]: De locaties.
        """
        return self._locations
    
    @property
    def distances(self) -> DataFrame:
        """
        Haal de afstanden op.

        Returns:
            DataFrame: De afstanden tussen locaties.
        """
        return self._distances
