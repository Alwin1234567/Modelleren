import pytest
from source.structures import Maps, Taak, Tijdslot, Long_time, Bak_kar_voorkeur
from source.locations import Hub, Ziekenhuis
from source.flow import Metrieken, Create_locations, Verbeteringen

def test_metrieken():
    # locaties maken
    hub = Hub("De Meern")
    ziekenhuis1 = Ziekenhuis("Equip Amsterdam", Bak_kar_voorkeur.BAK)
    ziekenhuis2 = Ziekenhuis("Annadal kliniek", Bak_kar_voorkeur.KAR)
    # taken maken
    taak_1 = Taak(Tijdslot(Long_time(5*60), Long_time(13*60)), ziekenhuis1, 230, 0)
    taak_2 = Taak(Tijdslot(Long_time(10*60), Long_time(17*60)), ziekenhuis1, 130, 0)
    taak_3 = Taak(Tijdslot(Long_time(4*60), Long_time(8*60)), ziekenhuis2, 90, 0)
    taak_4 = Taak(Tijdslot(Long_time(7*60), Long_time(12*60)), ziekenhuis2, 60, 0)
    taak_5 = Taak(Tijdslot(Long_time(14*60), Long_time(20*60)), ziekenhuis2, 120, 0)

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
    
    metriek = Metrieken([hub])
    for route in hub.routes:
        print('tijden:', route.start_tijd.tijd, route.eind_tijd.tijd, route.total_time)
    print('periodes:', metriek.uren_per_period(hub.routes))

def test_opslaan():
    hub = Hub("De Meern")
    ziekenhuis1 = Ziekenhuis("Equip Amsterdam", Bak_kar_voorkeur.BAK)
    ziekenhuis2 = Ziekenhuis("Annadal kliniek", Bak_kar_voorkeur.KAR)
    # taken maken
    taak_1 = Taak(Tijdslot(Long_time(5*60), Long_time(13*60)), ziekenhuis1, 230, 0)
    taak_2 = Taak(Tijdslot(Long_time(10*60), Long_time(17*60)), ziekenhuis1, 130, 0)
    taak_3 = Taak(Tijdslot(Long_time(4*60), Long_time(8*60)), ziekenhuis2, 90, 0)
    taak_4 = Taak(Tijdslot(Long_time(7*60), Long_time(12*60)), ziekenhuis2, 60, 0)
    taak_5 = Taak(Tijdslot(Long_time(14*60), Long_time(20*60)), ziekenhuis2, 120, 0)

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
    metriek = Metrieken([hub])
    for _ in range(4):
        metriek.add_iteratie()
    metriek.metrieken_to_csv()



def test_metrieken_met_verbeteren():
    create_locations = Create_locations()
    hubs = create_locations.hubs
    metrieken = Metrieken(hubs)
    verbeteringen = Verbeteringen(hubs, initial_heat=0.5, cooling_interval=5, metrieken=metrieken)
    verbeteringen.verbeteringen()
    metrieken.metrieken_to_csv()
    

# Run the test
if __name__ == "__main__":
    pytest.main()
