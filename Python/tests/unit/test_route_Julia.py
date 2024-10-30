import pytest
from source.transport import Route, Route_type
from source.structures import Distances, Maps, Coordinates
from source.locations import Hub, Ziekenhuis
from source.constants import Constants
from datetime import time

def test_avondroute_maken():
    # distances object maken
    hub1 = Hub("Hub1", Coordinates(52.076929, 5.107445))
    ziekenhuis1 = Ziekenhuis("B", Coordinates(52.366253, 4.873986), [4, 9, 0, 0, 2, 0, 0], [9, 9, 0, 0, 2, 0, 0])
    ziekenhuis2 = Ziekenhuis("C", Coordinates(52.252094, 4.797082), [8, 9, 0, 0, 2, 0, 0], [7, 9, 0, 0, 2, 0, 0])
    ziekenhuis3 = Ziekenhuis("D", Coordinates(52.215939, 5.174737), [4, 9, 0, 0, 2, 0, 0], [2, 9, 0, 0, 2, 0, 0])
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
    assert 92 < route_avond.total_distance < 93
    assert 85 < route_avond.total_time < 86
    assert 32 < route_avond.total_cost < 33
    # tijdelijke print controles
    print('route', route_avond.locations)
    print('distance', route_avond.total_distance)
    print('time', route_avond.total_time)
    print('cost', route_avond.total_cost)
    print('departuretimes', route_avond.departure_times)  

def test_ochtendroute_maken():
    # distances object maken
    hub1 = Hub("Hub1", Coordinates(52.076929, 5.107445))
    ziekenhuis1 = Ziekenhuis("B", Coordinates(52.366253, 4.873986), [4, 9, 0, 0, 2, 0, 0], [9, 9, 0, 0, 2, 0, 0])
    ziekenhuis2 = Ziekenhuis("C", Coordinates(52.252094, 4.797082), [8, 9, 0, 0, 2, 0, 0], [7, 9, 0, 0, 2, 0, 0])
    ziekenhuis3 = Ziekenhuis("D", Coordinates(52.215939, 5.174737), [4, 9, 0, 0, 2, 0, 0], [2, 9, 0, 0, 2, 0, 0])
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
    assert 83 < route_ochtend.total_distance < 84
    assert 82 < route_ochtend.total_time < 83
    assert 31 < route_ochtend.total_cost < 32
    # tijdelijke print controles
    print('route', route_ochtend.locations)
    print('distance', route_ochtend.total_distance)
    print('time', route_ochtend.total_time)
    print('cost', route_ochtend.total_cost)
    print('departuretimes', route_ochtend.departure_times)  

# Run the test
if __name__ == "__main__":
    pytest.main()
