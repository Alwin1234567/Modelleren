import pytest
from source.structures import LocationToCoordinates

def test_location():
    testlocatie = LocationToCoordinates()
    print(testlocatie.lat())
