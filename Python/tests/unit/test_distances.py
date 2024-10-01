import pytest
from source.structures import Distances, Maps, Coordinates
from source.locations import Location, Location_type
from source.constants import Constants

def test_distance_calculation():
    csv_file_path = Constants.CACHE_PATH / 'distance_time.csv'
    if csv_file_path.exists():
        csv_file_path.unlink()
    location1 = Location(Coordinates(52.076929, 5.107445), "A", Location_type.HUB)
    location2 = Location(Coordinates(52.366253, 4.873986), "B", Location_type.ZIEKENHUIS)
    location3 = Location(Coordinates(52.252094, 4.797082), "C", Location_type.ZIEKENHUIS)
    location4 = Location(Coordinates(52.215939, 5.174737), "D", Location_type.ZIEKENHUIS)
    distances_object = Distances()
    distances_object.add_location(location1)
    distances_object.add_location(location2)
    distances_object.add_location(location3)
    distances_object.add_location(location4)
    distances_object.generate_distances()
    assert 30 < distances_object.get_distance_time(location1, location2).time < 40
    assert 35 < distances_object.get_distance_time(location1, location2).distance < 45
    assert 25 < distances_object.get_distance_time(location4, location3).time < 35
    assert 25 < distances_object.get_distance_time(location4, location3).distance < 35
    Maps.disable_maps()

def test_distance_caching():
    location1 = Location(Coordinates(52.076929, 5.107445), "A", Location_type.HUB)
    location2 = Location(Coordinates(52.366253, 4.873986), "B", Location_type.ZIEKENHUIS)
    location3 = Location(Coordinates(52.252094, 4.797082), "C", Location_type.ZIEKENHUIS)
    location4 = Location(Coordinates(52.215939, 5.174737), "D", Location_type.ZIEKENHUIS)
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


# Run the test
if __name__ == "__main__":
    pytest.main()
