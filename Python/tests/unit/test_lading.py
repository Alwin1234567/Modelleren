import pytest
from source.structures import Lading_bak_kar, Auto_type, Bak_kar_voorkeur

def test_lading_bak_kar():
    lading = Lading_bak_kar(10, voorkeur=Bak_kar_voorkeur.BAK)
    assert lading.aantal_sets == 10
    assert lading.voorkeur_bak_kar == Bak_kar_voorkeur.BAK
    assert lading.aantal_bakken == 3
    assert lading.aantal_karren == 1
    
    assert lading.aantal(Auto_type.BAKWAGEN) == 1
    assert lading.aantal(Auto_type.BESTELBUS) == 3
    
    lading.set_voorkeur(Bak_kar_voorkeur.KAR)
    assert lading.voorkeur_bak_kar == Bak_kar_voorkeur.KAR
    assert lading.aantal_karren == 1
    assert lading.aantal(Auto_type.BAKWAGEN) == 1

# Run the test
if __name__ == "__main__":
    pytest.main()
