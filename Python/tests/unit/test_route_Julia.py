import pytest
from source.transport import Route, Route_type
from source.structures import Distances, Maps, Coordinates
from source.locations import Hub, Ziekenhuis
from source.constants import Constants
import datetime

def test_route_maken():
    # distances object maken
    hub1 = Hub("Hub", Coordinates(52.076929, 5.107445))
    ziekenhuis1 = Ziekenhuis("B", Coordinates(52.366253, 4.873986))
    ziekenhuis2 = Ziekenhuis("C", Coordinates(52.252094, 4.797082))
    ziekenhuis3 = Ziekenhuis("D", Coordinates(52.215939, 5.174737))
    distances_object = Distances()
    distances_object.add_location(hub1)
    distances_object.add_location(ziekenhuis1)
    distances_object.add_location(ziekenhuis2)
    distances_object.add_location(ziekenhuis3)
    #distances_object.generate_distances()
    #Maps.disable_maps()
    print(distances_object.locations)
    print(distances_object.distances)

    toe_te_voegen_ziekenhuizen = [ziekenhuis1, ziekenhuis2, ziekenhuis3]

    route_object = Route(Route_type.AVOND, hub1, distances_object)
    assert route_object.route_type == Route_type.AVOND
    print(route_object.route_type)
    
    print(route_object.start_tijd)
    print(route_object.locations)
    print(route_object.start)

    #route maken
    route_object.make_route(toe_te_voegen_ziekenhuizen)
    

# Run the test
if __name__ == "__main__":
    pytest.main()
