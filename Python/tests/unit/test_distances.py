import pytest
from source.structures import Distances, Maps, Coordinates
from source.locations import Location, Location_type
from source.constants import Constants
from datetime import time

def test_distance_calculation():
    csv_file_path = Constants.CACHE_PATH / 'distance_time.csv'
    if csv_file_path.exists():
        csv_file_path.unlink()
    location1 = Location("De Meern", Location_type.HUB)
    location2 = Location("A Klinieken", Location_type.ZIEKENHUIS)
    location3 = Location("Andros Clinics Rijswijk", Location_type.ZIEKENHUIS)
    location4 = Location("Annadal kliniek", Location_type.ZIEKENHUIS)
    distances_object = Distances()
    distances_object.add_location(location1)
    distances_object.add_location(location2)
    distances_object.add_location(location3)
    distances_object.add_location(location4)
    distances_object.generate_distances()
    assert 15 < distances_object.get_distance_time(location1, location2).time < 25
    assert 10 < distances_object.get_distance_time(location1, location2).distance < 20
    assert 150 < distances_object.get_distance_time(location4, location3).time < 160
    assert 210 < distances_object.get_distance_time(location4, location3).distance < 220
    Maps.disable_maps()

def test_distance_caching():
    location1 = Location("De Meern", Location_type.HUB)
    location2 = Location("A Klinieken", Location_type.ZIEKENHUIS)
    location3 = Location("Andros Clinics Rijswijk", Location_type.ZIEKENHUIS)
    location4 = Location("Annadal kliniek", Location_type.ZIEKENHUIS)
    distances_object = Distances()
    distances_object.add_location(location1)
    distances_object.add_location(location2)
    distances_object.add_location(location3)
    distances_object.add_location(location4)
    distances_object.generate_distances()
    Maps.disable_maps()
    distances_object = Distances()
    distances_object.add_location(location1)
    distances_object.add_location(location2)
    distances_object.add_location(location3)
    distances_object.add_location(location4)
    distances_object.generate_distances()
    assert Maps.is_enabled() == False
    csv_file_path = Constants.CACHE_PATH / 'distance_time.csv'
    assert csv_file_path.exists(), f"{csv_file_path} does not exist"

def test_available_locations():
    location1 = Location("De Meern", Location_type.HUB)
    location2 = Location("A Klinieken", Location_type.ZIEKENHUIS)
    location3 = Location("Andros Clinics Rijswijk", Location_type.ZIEKENHUIS)
    location4 = Location("Annadal kliniek", Location_type.ZIEKENHUIS)
    distances_object = Distances()
    distances_object.add_location(location1)
    distances_object.add_location(location2)
    distances_object.add_location(location3)
    distances_object.add_location(location4)
    distances_object.generate_distances()

    start_time = time(10, 0)
    skip_locations = [location2]
    available_locs = list(distances_object.available_locations(location1, skip_locations, start_time))

    # Check that the correct locations are returned
    assert len(available_locs) == 2
    names = [loc.name for loc, _ in available_locs]
    assert "Andros Clinics Rijswijk" in names	
    assert "Annadal kliniek" in names

    # Check that the locations are sorted by cost
    assert available_locs[0][1].cost(start_time) < available_locs[1][1].cost(start_time)


# Run the test
if __name__ == "__main__":
    pytest.main()
