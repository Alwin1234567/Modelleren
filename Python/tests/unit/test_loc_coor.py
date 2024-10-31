import pytest
from source.locations import Location, Location_type

def test_location_2():
    bestaand_ziekenhuis = 'A Klinieken'
    nietbestaand_ziekenhuis = 'Niet-bestaand Ziekenhuis'
    postcode_onbekend_ziekenhuis = 'Koning Kliniek'
    coordinaten = Location(bestaand_ziekenhuis, Location_type.ZIEKENHUIS).name_to_coordinates()
    
    assert 52.10 <= coordinaten.lat <= 52.12
    assert 5.24 <= coordinaten.lon <= 5.26
    with pytest.raises(Exception, match="Deze locatie is niet bekend."):
        Location(nietbestaand_ziekenhuis, Location_type.ZIEKENHUIS).name_to_coordinates()
    with pytest.raises(Exception, match="Van deze locatie is geen postcode bekend."):
        Location(postcode_onbekend_ziekenhuis, Location_type.ZIEKENHUIS).name_to_coordinates()

# Run the test
if __name__ == "__main__":
    pytest.main()
