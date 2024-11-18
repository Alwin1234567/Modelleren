import pytest
from source.transport import Route
from source.structures import Distances, Maps, Taak, Tijdslot, Long_time
from source.locations import Hub, Ziekenhuis

def test_route_maken():
    # distances object maken
    hub1 = Hub("De Meern")
    ziekenhuis1 = Ziekenhuis("A Klinieken", postcode = "3712 BP")
    ziekenhuis2 = Ziekenhuis("Andros Clinics Rijswijk", postcode = "2289 CA")
    ziekenhuis3 = Ziekenhuis("Annadal kliniek", postcode = "6216 EG")
    distances_object = Distances()
    distances_object.add_location(hub1)
    distances_object.add_location(ziekenhuis1)
    distances_object.add_location(ziekenhuis2)
    distances_object.add_location(ziekenhuis3)
    distances_object.generate_distances()
    Maps.disable_maps()

    # taken maken
    taak1 = Taak(Tijdslot(Long_time(10*60), Long_time(12*60)), ziekenhuis1, 4, 9, Tijdslot(Long_time(34*60), Long_time(36*60)))
    taak2 = Taak(Tijdslot(Long_time(8*60), Long_time(9*60)), ziekenhuis2, 8, 7, Tijdslot(Long_time(30*60), Long_time(36*60)))
    taak3 = Taak(Tijdslot(Long_time(8*60), Long_time(10*60)), ziekenhuis3, 4, 2, Tijdslot(Long_time(30*60), Long_time(36*60)))
    taak4 = Taak(Tijdslot(Long_time(3*60), Long_time(4*60)), ziekenhuis1, 6, 6, Tijdslot(Long_time(58*60), Long_time(60*60)))
    taak5 = Taak(Tijdslot(Long_time(32*60), Long_time(38*60)), ziekenhuis2, 5, 3, Tijdslot(Long_time(39*60), Long_time(46*60)))
    taak6 = Taak(Tijdslot(Long_time(11*60), Long_time(18*60)), ziekenhuis3, 4, 9, Tijdslot(Long_time(39*60), Long_time(46*60)))
    taken = [taak1, taak2, taak3, taak4, taak5, taak6]

    route = Route(hub1, distances_object, 35)
    route.maak_route(taak1, taken[1:])
    
    assert Tijdslot(Long_time(3*60), Long_time(4*60)).is_in_tijdvak(route.start_tijd)
    assert Tijdslot(Long_time(14*60), Long_time(15*60)).is_in_tijdvak(route.eind_tijd)
    assert 510 < route.total_distance < 520
    assert 660 < route.total_time < 670
    assert 270 < route.total_cost < 280
    
    taakvolgorde = [taak4, taak2, taak1, taak6]
    for i in range(len(route.departure_times)):
        # taken in juiste volgorde ingepland en vertrektijden bij ziekenhuizen binnen tijdvakken?
        assert route.departure_times[i][0] == taakvolgorde[i]
        assert taakvolgorde[i].tijdslot.is_in_tijdvak(route.departure_times[i][1])

def test_route_maken_uitproberen():
    # distances object maken
    hub1 = Hub("De Meern")
    ziekenhuis1 = Ziekenhuis("A Klinieken", postcode = "3712 BP")
    ziekenhuis2 = Ziekenhuis("Andros Clinics Rijswijk", postcode = "2289 CA")
    ziekenhuis3 = Ziekenhuis("Annadal kliniek", postcode = "6216 EG")
    distances_object = Distances()
    distances_object.add_location(hub1)
    distances_object.add_location(ziekenhuis1)
    distances_object.add_location(ziekenhuis2)
    distances_object.add_location(ziekenhuis3)
    distances_object.generate_distances()
    Maps.disable_maps()

    # taken maken
    taak1 = Taak(Tijdslot(Long_time(10*60), Long_time(12*60)), ziekenhuis1, 4, 9, Tijdslot(Long_time(34*60), Long_time(36*60)))
    taak2 = Taak(Tijdslot(Long_time(8*60), Long_time(9*60)), ziekenhuis2, 8, 7, Tijdslot(Long_time(30*60), Long_time(36*60)))
    taak3 = Taak(Tijdslot(Long_time(8*60), Long_time(10*60)), ziekenhuis3, 4, 2, Tijdslot(Long_time(30*60), Long_time(36*60)))
    taak4 = Taak(Tijdslot(Long_time(3*60), Long_time(4*60)), ziekenhuis1, 6, 6, Tijdslot(Long_time(58*60), Long_time(60*60)))
    taak5 = Taak(Tijdslot(Long_time(32*60), Long_time(38*60)), ziekenhuis2, 5, 3, Tijdslot(Long_time(39*60), Long_time(46*60)))
    taak6 = Taak(Tijdslot(Long_time(11*60), Long_time(18*60)), ziekenhuis3, 4, 9, Tijdslot(Long_time(39*60), Long_time(46*60)))
    taken = [taak1, taak2, taak3, taak4, taak5, taak6]

    route = Route(hub1, distances_object, 35)
    
    route.maak_route(taak1, taken[1:])
    
    print('starttijd', route.start_tijd.tijd, 'dag:', route.start_tijd.dag)
    print('eindtijd', route.eind_tijd.tijd, 'dag:', route.eind_tijd.dag)
    print('distance', route.total_distance)
    print('time', route.total_time)
    print('cost', route.total_cost)
    print('departuretimes')
    for d in route.departure_times:
        print(d[0].ziekenhuis, d[1].tijd, d[0].brengen, d[0].halen)

# Run the test
if __name__ == "__main__":
    pytest.main()
