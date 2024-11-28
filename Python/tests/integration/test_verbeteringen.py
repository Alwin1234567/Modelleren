from source.flow import Verbeteringen, Create_locations
from copy import deepcopy
import pytest
from source.structures import Status

def test_verbeteringen():
    create_locations = Create_locations()
    hubs = deepcopy(create_locations.hubs)
    verbeteringen = Verbeteringen(create_locations.hubs, initial_heat=0.5, cooling_interval=5)
    assert verbeteringen.status == Status.PREPARING
    verbeteringen.verbeteringen()
    assert verbeteringen.status == Status.FINISHED
    verbeterde_hubs = verbeteringen._hubs
    for verbeterde_hub, hub in zip(verbeterde_hubs, hubs):
        assert verbeterde_hub.cost < hub.cost

if __name__ == '__main__':
    pytest.main()
