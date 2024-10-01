import pytest
from source.structures import LocationToCoordinates, ReadLocation, Coordinates

def test_location():
    #bestaande postcode
    postcode_bestaand = '2289 CA'
    coordinates_bestaand = LocationToCoordinates(postcode_bestaand).lat_lon_from_postcode()
    assert coordinates_bestaand.coordinates == Coordinates(52.04832912, 4.34559652).coordinates

    #bestaande postcode zonder spatie
    postcode_bestaand_2 = '2289CA'
    coordinates_bestaand_2 = LocationToCoordinates(postcode_bestaand_2).lat_lon_from_postcode()
    assert coordinates_bestaand_2.coordinates == Coordinates(52.04832912, 4.34559652).coordinates

    #niet-bestaande postcode
    postcode_nietbestaand = '2289 SD'
    coordinates_nietbestaand = LocationToCoordinates(postcode_nietbestaand).lat_lon_from_postcode()
    assert coordinates_nietbestaand == None

    #niet-Nederlandse postcode
    postcode_nietbestaand_2 = '2289'
    coordinates_nietbestaand_2 = LocationToCoordinates(postcode_nietbestaand_2).lat_lon_from_postcode()
    assert coordinates_nietbestaand_2 == None

def test_csv_loc():
    bestaand_ziekenhuis = 'Equipe Den Haag'
    nietbestaand_ziekenhuis = 'Niet-bestaand Ziekenhuis'
    postcode_onbekend_ziekenhuis = 'A klinieken'
    
    assert ReadLocation(bestaand_ziekenhuis).postcode() == '2514 DH'
    assert ReadLocation(nietbestaand_ziekenhuis).postcode() == None
    assert ReadLocation(postcode_onbekend_ziekenhuis).postcode() == None



# Run the test
if __name__ == "__main__":
    pytest.main()
