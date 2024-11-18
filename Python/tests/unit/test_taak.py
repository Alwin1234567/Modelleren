import pytest
from datetime import time
from source.structures import Taak, Tijdslot, Long_time, Distances, Cost
from source.constants import Constants
from unittest.mock import MagicMock
import numpy as np

@pytest.fixture
def mock_distances():
    distances = MagicMock(spec=Distances)
    distances.has_location.return_value = True
    distances.get_distance.return_value = 10  # Example distance in km
    distances.get_time.return_value = Long_time(30)  # Example time in minutes
    return distances

@pytest.fixture
def mock_ziekenhuis():
    return MagicMock()

@pytest.fixture
def tijdslot():
    return Tijdslot(Long_time(480), Long_time(600))  # 8:00 to 10:00

@pytest.fixture
def taak(tijdslot, mock_ziekenhuis):
    return Taak(tijdslot, mock_ziekenhuis, brengen=5, halen=3)

def test_init(taak, tijdslot, mock_ziekenhuis):
    assert taak.tijdslot == tijdslot
    assert taak.ziekenhuis == mock_ziekenhuis
    assert taak.brengen == 5
    assert taak.halen == 3
    assert taak.halen_brengen == 8

def test_cost_with_taak(taak, mock_distances, tijdslot, mock_ziekenhuis):
    # Create another task to compare with
    other_taak = Taak(tijdslot, mock_ziekenhuis, brengen=2, halen=4)
    other_taak._ingeplande_tijd = Long_time(600)  # 10:00

    # Set the current task's scheduled time
    taak._ingeplande_tijd = Long_time(480)  # 8:00

    # Mock the cost calculation
    Cost.calculate_cost_time = MagicMock(return_value=50)  # Example time cost

    # Test cost calculation with end=True
    cost = taak.cost_with_taak(other_taak, mock_distances, end=True)
    assert cost == 10 * Constants.PRIJS_PER_KM + 50

    # Test cost calculation with end=False
    cost = taak.cost_with_taak(other_taak, mock_distances, end=False)
    assert cost == np.inf

def test_invalid_cost_with_taak(taak, mock_distances, tijdslot, mock_ziekenhuis):
    # Create another task to compare with
    other_taak = Taak(tijdslot, mock_ziekenhuis, brengen=2, halen=4)

    # Test without scheduled time
    with pytest.raises(ValueError):
        taak.cost_with_taak(other_taak, mock_distances)

    # Set the current task's scheduled time
    taak._ingeplande_tijd = Long_time(480)  # 8:00

    # Test with unknown location
    mock_distances.has_location.return_value = False
    with pytest.raises(ValueError):
        taak.cost_with_taak(other_taak, mock_distances)

if __name__ == '__main__':
    pytest.main()
