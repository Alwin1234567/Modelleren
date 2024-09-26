import pytest
from source.constants import Constants

def test_constants():
    c = Constants()
    assert c.prijs_per_km == 0.0
    assert c.prijs_per_uur_chauffeur == 0.0
    assert c.tijdsduur_inladen_en_uitladen_plat == 0.0
    assert c.tijdsduur_inladen_en_uitladen_instrumentensets == 0.0
    assert c.capaciteit_voertuig == 0
    assert c.tijdsduur_inladen_en_uitladen(100) == 0.0
    assert c.rijkosten(100.0, 100.0) == 0.0
