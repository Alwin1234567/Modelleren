import pytest
from source.constants import Constants

def test_constants():
    assert Constants.PRIJS_PER_KM == 0.0
    assert Constants.PRIJS_PER_UUR_CHAUFFEUR == 0.0
    assert Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT == 0.0
    assert Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_INSTRUMENTENSETS == 0.0
    assert Constants.CAPACITEIT_VOERTUIG == 0
    assert Constants.MAPS_URL == "http://localhost:8989/route"
    assert Constants.MAPS_PARAMS == {
        'profile': 'car',
        'locale': 'en',
        'calc_points': 'false'
    }
    assert Constants.STARTUP_WAIT_TIME == 5

# Run the test
if __name__ == "__main__":
    pytest.main()
