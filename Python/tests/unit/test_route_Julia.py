import pytest
from source.transport import Route, Route_type
from source.structures import Distances, Maps, Coordinates
from source.locations import Hub, Ziekenhuis
from source.constants import Constants
import datetime

def test_route_maken():
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

    route_object = Route(Route_type.AVOND, hub1, distances_object, 11)
    assert route_object.route_type == Route_type.AVOND
    
    print('starttijd', route_object.start_tijd)
    print('route', route_object.locations)
    print('startlocatie', route_object.start)
    print('distance', route_object.total_distance)
    print('time', route_object.total_time)
    print('cost', route_object.total_cost)

    #route maken
    route_object.make_route([], 'monday')
    print('route', route_object.locations)
    print('distance', route_object.total_distance)
    print('time', route_object.total_time)
    print('cost', route_object.total_cost)
    print('departuretimes', route_object.departure_times)  

    route_object_ochtend = Route(Route_type.OCHTEND, hub1, distances_object, 19)
    #route maken
    route_object_ochtend.make_route([], 'monday')
    print('route', route_object_ochtend.locations)
    print('distance', route_object_ochtend.total_distance)
    print('time', route_object_ochtend.total_time)
    print('cost', route_object_ochtend.total_cost)
    print('departuretimes', route_object_ochtend.departure_times)  
    
# Run the test
if __name__ == "__main__":
    pytest.main()
