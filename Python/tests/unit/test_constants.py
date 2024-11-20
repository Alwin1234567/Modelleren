import pytest
from source.constants import Constants
from source.structures import Auto_type, Bak_kar_voorkeur

def test_constants():
    assert isinstance(Constants.prijs_per_km(Auto_type.BAKWAGEN), float)
    assert isinstance(Constants.PRIJS_PER_UUR_CHAUFFEUR, float)
    assert isinstance(Constants.TIJDSDUUR_INLADEN_EN_UITLADEN_PLAT, float)
    assert isinstance(Constants.tijdsduur_in_en_uitladen(Bak_kar_voorkeur.BAK), float)
    assert isinstance(Constants.capaciteit_auto(Auto_type.BAKWAGEN), int)
    assert isinstance(Constants.capaciteit_bak_kar(Bak_kar_voorkeur.BAK), int)
    assert isinstance(Constants.MAPS_URL, str)
    assert isinstance(Constants.MAPS_PARAMS, dict)
    assert isinstance(Constants.STARTUP_WAIT_TIME, int)

# Run the test
if __name__ == "__main__":
    pytest.main()
