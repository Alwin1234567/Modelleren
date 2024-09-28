import pytest
from source.structures import LocationToCoordinates

def test_location():
    postcode_nietbestaand = '2289 SD'
    postcode_bestaand = '2289CA'
    testlocatie = LocationToCoordinates(postcode_nietbestaand)
    print("adres, postcode, werkelijk")
    print(testlocatie.lat_lon_from_adress())
    print(testlocatie.lat_lon_from_postcode())
    print("(52.0484169, 4.3451929)")

def test_Julia():
    lat = 50.5000000
    print(50 < lat < 54.5000)

# Run the test
if __name__ == "__main__":
    pytest.main()
