import pytest
from source.constants import Constants

def test_constants():
    assert isinstance(Constants.PRIJS_PER_KM, float)
    assert isinstance(Constants.PRIJS_PER_UUR_CHAUFFEUR, float)
    assert isinstance(Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT, float)
    assert isinstance(Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_INSTRUMENTENSETS, float)
    assert isinstance(Constants.CAPACITEIT_VOERTUIG, int)
    assert isinstance(Constants.MAPS_URL, str)
    assert isinstance(Constants.MAPS_PARAMS, dict)
    assert isinstance(Constants.STARTUP_WAIT_TIME, int)

# Run the test
if __name__ == "__main__":
    pytest.main()
