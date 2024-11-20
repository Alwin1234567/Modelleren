import pytest
from source.structures import Maps, Taak, Tijdslot, Long_time, Bak_kar_voorkeur
from source.locations import Hub, Ziekenhuis
import time

def test_routes_splitsen():
    # locaties maken
    hub = Hub("De Meern")
    ziekenhuis1 = Ziekenhuis("Equip Amsterdam", Bak_kar_voorkeur.BAK)
    ziekenhuis2 = Ziekenhuis("Annadal kliniek", Bak_kar_voorkeur.KAR)
    ziekenhuis3 = Ziekenhuis("Annatommie Amstelveen", Bak_kar_voorkeur.KAR)
    ziekenhuis4 = Ziekenhuis("Annatommie Utrecht", Bak_kar_voorkeur.KAR)
    # taken maken
    taak_1 = Taak(Tijdslot(Long_time(5*60), Long_time(13*60)), ziekenhuis1, 180, 0)
    taak_2 = Taak(Tijdslot(Long_time(10*60), Long_time(17*60)), ziekenhuis1, 90, 0)
    taak_3 = Taak(Tijdslot(Long_time(4*60), Long_time(8*60)), ziekenhuis1, 0, 20)
    taak_4 = Taak(Tijdslot(Long_time(7*60), Long_time(12*60)), ziekenhuis2, 60, 0)
    taak_5 = Taak(Tijdslot(Long_time(14*60), Long_time(20*60)), ziekenhuis2, 80, 0)
    taak_6 = Taak(Tijdslot(Long_time(5*60), Long_time(13*60)), ziekenhuis2, 0, 70)
    taak_7 = Taak(Tijdslot(Long_time(10*60), Long_time(17*60)), ziekenhuis3, 0, 100)
    taak_8 = Taak(Tijdslot(Long_time(4*60), Long_time(8*60)), ziekenhuis3, 90, 0)
    taak_9 = Taak(Tijdslot(Long_time(7*60), Long_time(12*60)), ziekenhuis3, 30, 0)
    taak_10 = Taak(Tijdslot(Long_time(14*60), Long_time(20*60)), ziekenhuis4, 50, 0)

    # taken aan ziekenhuizen toevoegen
    ziekenhuis1.add_taak(taak_1)
    ziekenhuis1.add_taak(taak_2)
    ziekenhuis1.add_taak(taak_3)
    ziekenhuis2.add_taak(taak_4)
    ziekenhuis2.add_taak(taak_5)
    ziekenhuis2.add_taak(taak_6)
    ziekenhuis3.add_taak(taak_7)
    ziekenhuis3.add_taak(taak_8)
    ziekenhuis3.add_taak(taak_9)
    ziekenhuis4.add_taak(taak_10)
    # ziekenhuizen aan hub toevoegen
    hub.add_ziekenhuis(ziekenhuis1)
    hub.add_ziekenhuis(ziekenhuis2)
    hub.add_ziekenhuis(ziekenhuis3)
    hub.add_ziekenhuis(ziekenhuis4)

    # distances berekenen en routes startoplossing maken
    hub.finish_creation()
    Maps.disable_maps()

    hub.fill_autos()
    assert len(hub.routes) == 4
    assert len(hub.autos) == 3

    # splitsen
    hub.split_routes()
    hub.fill_autos()
    assert len(hub.routes) == 6
    assert len(hub.autos) == 3

    # nogmaals splitsen
    hub.split_routes()
    hub.fill_autos()
    assert len(hub.routes) == 7
    assert len(hub.autos) == 3


# Run the test
if __name__ == "__main__":
    pytest.main()
