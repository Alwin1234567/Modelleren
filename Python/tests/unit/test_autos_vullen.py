import pytest
from source.structures import Maps, Taak, Tijdslot, Long_time, Bak_kar_voorkeur
from source.locations import Hub, Ziekenhuis

def test_autos_vullen():
    # locaties maken
    hub = Hub("De Meern")
    ziekenhuis1 = Ziekenhuis("Equip Amsterdam", Bak_kar_voorkeur.BAK)
    ziekenhuis2 = Ziekenhuis("Annadal kliniek", Bak_kar_voorkeur.KAR)
    # taken maken
    taak_1 = Taak(Tijdslot(Long_time(5*60), Long_time(13*60)), ziekenhuis1, 28, 0)
    taak_2 = Taak(Tijdslot(Long_time(10*60), Long_time(17*60)), ziekenhuis1, 17, 0)
    taak_3 = Taak(Tijdslot(Long_time(4*60), Long_time(8*60)), ziekenhuis2, 21, 0)
    taak_4 = Taak(Tijdslot(Long_time(7*60), Long_time(12*60)), ziekenhuis2, 15, 0)
    taak_5 = Taak(Tijdslot(Long_time(14*60), Long_time(20*60)), ziekenhuis2, 26, 0)

    # taken aan ziekenhuizen toevoegen
    ziekenhuis1.add_taak(taak_1)
    ziekenhuis1.add_taak(taak_2)
    ziekenhuis2.add_taak(taak_3)
    ziekenhuis2.add_taak(taak_4)
    ziekenhuis2.add_taak(taak_5)
    # ziekenhuizen aan hub toevoegen
    hub.add_ziekenhuis(ziekenhuis1)
    hub.add_ziekenhuis(ziekenhuis2)

    # distances berekenen en routes startoplossing maken
    hub.finish_creation()
    Maps.disable_maps()

    # auto's vullen met routes
    hub.fill_autos()
    
    assert len(hub.routes) == 4
    assert len(hub.autos) == 3

    geplaatste_routes = []
    for auto in hub.autos:
        for route in auto.routes:
            geplaatste_routes.append(route)
    
    for route in hub.routes:
        # controleer of alle routes van de hub in een auto zijn geplaatst
        assert route in geplaatste_routes

# Run the test
if __name__ == "__main__":
    pytest.main()
