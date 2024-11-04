import pytest
from source.transport import Route, Route_type
from source.structures import Distances, Maps, Coordinates, Taak, Tijdslot, Long_time
from source.locations import Hub, Ziekenhuis
from source.constants import Constants
from datetime import time


def test_route_maken4():
    ziekenhuis1 = Ziekenhuis("A Klinieken", [4, 9, 0, 0, 2, 0, 0], [9, 9, 0, 0, 2, 0, 0], postcode = "3712 BP")
    taak1 = Taak(Tijdslot(Long_time(10*60), Long_time(12*60)), ziekenhuis1, 4, 9, Tijdslot(Long_time(34*60), Long_time(36*60)))
    print(taak1.laadtijd)

def test_route_maken2():
    # distances object maken
    hub1 = Hub("De Meern")
    ziekenhuis1 = Ziekenhuis("A Klinieken", [4, 9, 0, 0, 2, 0, 0], [9, 9, 0, 0, 2, 0, 0], postcode = "3712 BP")
    ziekenhuis2 = Ziekenhuis("Andros Clinics Rijswijk", [8, 5, 0, 0, 2, 0, 0], [7, 3, 0, 0, 2, 0, 0], postcode = "2289 CA")
    ziekenhuis3 = Ziekenhuis("Annadal kliniek", [4, 9, 0, 0, 2, 0, 0], [2, 9, 0, 0, 2, 0, 0], postcode = "6216 EG")
    distances_object = Distances()
    distances_object.add_location(hub1)
    distances_object.add_location(ziekenhuis1)
    distances_object.add_location(ziekenhuis2)
    distances_object.add_location(ziekenhuis3)
    distances_object.generate_distances()
    Maps.disable_maps()

    print('taken maken')
    # taken maken
    taak1 = Taak(Tijdslot(Long_time(10*60), Long_time(12*60)), ziekenhuis1, 4, 9, Tijdslot(Long_time(34*60), Long_time(36*60)))
    taak2 = Taak(Tijdslot(Long_time(8*60), Long_time(10*60)), ziekenhuis2, 8, 7, Tijdslot(Long_time(34*60), Long_time(36*60)))
    taak3 = Taak(Tijdslot(Long_time(8*60), Long_time(10*60)), ziekenhuis3, 4, 2, Tijdslot(Long_time(34*60), Long_time(36*60)))
    taak4 = Taak(Tijdslot(Long_time(3*60), Long_time(4*60)), ziekenhuis1, 9, 9, Tijdslot(Long_time(58*60), Long_time(60*60)))
    taak5 = Taak(Tijdslot(Long_time(10*60), Long_time(12*60)), ziekenhuis2, 5, 3, Tijdslot(Long_time(34*60), Long_time(36*60)))
    taak6 = Taak(Tijdslot(Long_time(10*60), Long_time(12*60)), ziekenhuis3, 4, 9, Tijdslot(Long_time(34*60), Long_time(36*60)))
    print('lijst maken')
    taken = [taak1, taak2, taak3, taak4, taak5, taak6]

    route = Route(Route_type.AVOND, hub1, distances_object, 20)
    max_wegbrengen = 20-9
    max_ophalen = 20-9
    print('vooraan toe te voegen')
    taak1.set_begintijd_taak(taak1.tijdslot.starttijd)
    #for taak in taken[1:]:
     #   if taak.tijdslot.eindtijd < taak1.begintijd_taak:
      #      print('buiten tijdslot')
       # gefilterd = list(filter(lambda taak: taak.tijdslot.eindtijd < taak1.begintijd_taak and taak.brengen <= max_wegbrengen and taak.halen <= max_ophalen, taken))

    route.vooraan_toe_te_voegen(taken[1:], taak1, taak1, 20-9, 20-9, Long_time(34*60))

    print('route maken')
    #route.maak_route_2(taak1, taken[1:])
    

def test_avondroute_maken():
    # distances object maken
    hub1 = Hub("De Meern")
    ziekenhuis1 = Ziekenhuis("A Klinieken", [4, 9, 0, 0, 2, 0, 0], [9, 9, 0, 0, 2, 0, 0])
    ziekenhuis2 = Ziekenhuis("Andros Clinics Rijswijk", [8, 9, 0, 0, 2, 0, 0], [7, 9, 0, 0, 2, 0, 0])
    ziekenhuis3 = Ziekenhuis("Annadal kliniek", [4, 9, 0, 0, 2, 0, 0], [2, 9, 0, 0, 2, 0, 0])
    distances_object = Distances()
    distances_object.add_location(hub1)
    distances_object.add_location(ziekenhuis1)
    distances_object.add_location(ziekenhuis2)
    distances_object.add_location(ziekenhuis3)
    distances_object.generate_distances()
    Maps.disable_maps()

    route_avond = Route(Route_type.AVOND, hub1, distances_object, 11)
    # startwaarden controleren
    assert route_avond.route_type == Route_type.AVOND
    assert route_avond.start_tijd == time(17,0)
    assert route_avond.locations == []
    assert route_avond.start == hub1
    assert route_avond.total_distance == 0
    assert route_avond.total_time == 0
    assert route_avond.total_cost == 0

    # route maken
    route_avond.make_route([], 'monday')
    assert 30 < route_avond.total_distance < 40
    assert 30 < route_avond.total_time < 40
    assert 10 < route_avond.total_cost < 20
    # tijdelijke print controles
    print('route', route_avond.locations)
    print('distance', route_avond.total_distance)
    print('time', route_avond.total_time)
    print('cost', route_avond.total_cost)
    print('departuretimes', route_avond.departure_times)  

def test_ochtendroute_maken():
    # distances object maken
    hub1 = Hub("De Meern")
    ziekenhuis1 = Ziekenhuis("A Klinieken", [4, 9, 0, 0, 2, 0, 0], [9, 9, 0, 0, 2, 0, 0])
    ziekenhuis2 = Ziekenhuis("Andros Clinics Rijswijk", [8, 9, 0, 0, 2, 0, 0], [7, 9, 0, 0, 2, 0, 0])
    ziekenhuis3 = Ziekenhuis("Annadal kliniek", [4, 9, 0, 0, 2, 0, 0], [2, 9, 0, 0, 2, 0, 0])
    distances_object = Distances()
    distances_object.add_location(hub1)
    distances_object.add_location(ziekenhuis1)
    distances_object.add_location(ziekenhuis2)
    distances_object.add_location(ziekenhuis3)
    distances_object.generate_distances()
    Maps.disable_maps() 

    route_ochtend = Route(Route_type.OCHTEND, hub1, distances_object, 19)
    assert route_ochtend.route_type == Route_type.OCHTEND
    assert route_ochtend.start_tijd == time(7,0)
    
    route_ochtend.make_route([], 'monday')
    assert 30 < route_ochtend.total_distance < 40
    assert 30 < route_ochtend.total_time < 40
    assert 10 < route_ochtend.total_cost < 20
    # tijdelijke print controles
    print('route', route_ochtend.locations)
    print('distance', route_ochtend.total_distance)
    print('time', route_ochtend.total_time)
    print('cost', route_ochtend.total_cost)
    print('departuretimes', route_ochtend.departure_times)  

# Run the test
if __name__ == "__main__":
    pytest.main()
