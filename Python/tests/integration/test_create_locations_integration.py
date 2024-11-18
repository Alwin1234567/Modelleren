import pytest
import pandas as pd
from source.flow import Create_locations
from source.constants import Constants
from source.locations import Ziekenhuis, Hub
from source.structures import Status, Maps

def test_create_locations():
    # Arrange
    create_locations = Create_locations()
    
    # test if all hubs are of type hub
    for location in create_locations.hubs:
        assert isinstance(location, Hub)
    
    # test if status is set to finished
    assert create_locations.status == Status.FINISHED

if __name__ == '__main__':
    pytest.main()
