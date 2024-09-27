import pytest
from source.structures import Maps, Coordinates, Distance_time
from source.constants import Constants
import requests

def test_maps_enabling():
    assert not Maps.is_enabled()
    Maps.enable_maps()
    assert Maps.is_enabled()
    Maps.disable_maps()
    assert not Maps.is_enabled()

def test_maps_calculating():
    coordinates1 = Coordinates(52.078828, 5.150504)
    coordinates2 = Coordinates(52.354679, 4.887852)

    assert not Maps.is_enabled()
    if not Maps.is_enabled():
        Maps.enable_maps()
    assert Maps.is_enabled()
    
    url = f"{Constants.MAPS_URL}?{coordinates1.OSMR_str}&{coordinates2.OSMR_str}&profile={Constants.MAPS_PARAMS['profile']}&locale={Constants.MAPS_PARAMS['locale']}&calc_points={Constants.MAPS_PARAMS['calc_points']}"
    assert url == "http://localhost:8989/route?point=52.078828,5.150504&point=52.354679,4.887852&profile=car&locale=en&calc_points=false"

    response = requests.get(url)
    result = Distance_time(1e10, 1e10)
    assert response.status_code == 200

    data = response.json()

    assert 'paths' in data
    assert len(data['paths']) > 0

    path = data['paths'][0]
    distance: float = path['distance']/1000  # Distance in kilometers
    time: float = path['time']/1000/60  # Time in minutes
    result = Distance_time(distance, time)
    
    assert 41 < result.distance < 42
    assert 30 < result.time < 40
    assert Maps.is_enabled()
    Maps.disable_maps()
    assert not Maps.is_enabled()


# Run the test
if __name__ == "__main__":
    pytest.main()
