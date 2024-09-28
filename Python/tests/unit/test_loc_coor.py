import pytest
from source.structures import LocationToCoordinates
from source.structures import ReadLocation

def test_location():
    postcode_nietbestaand = '2289 SD'
    postcode_bestaand = '2289CA'
    testlocatie = LocationToCoordinates(postcode_bestaand)
    print("adres, postcode, werkelijk")
    print(testlocatie.lat_lon_from_adress())
    print(testlocatie.lat_lon_from_postcode())
    print("(52.0484169, 4.3451929)")

def test_csv_loc():
    print("-")
    name_ziekenhuis = 'Equipe Den Haag' #'Andros Clinics' # 'Flex clinics' # 
    postcode_loc = ReadLocation(name_ziekenhuis)
    print(postcode_loc.postcode())


# Run the test
if __name__ == "__main__":
    pytest.main()
