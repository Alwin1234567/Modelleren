import pytest
from datetime import time
from source.structures import Cost, Auto_type
from source.constants import Constants
from datetime import timedelta, datetime

def test_calculate_cost_time():
    # Test during day shift
    start_time = Constants.TIJD_DAG[0]  # 9:00 AM
    duration_minutes = 2*60  # 2 hours
    expected_cost = 2 * Constants.PRIJS_PER_UUR_CHAUFFEUR  # No extra cost during day shift
    assert Cost.calculate_cost_time(start_time, duration_minutes) == pytest.approx(expected_cost)

    # Test part day, part evening shift
    day_end = Constants.TIJD_DAG[1]
    start_time = day_end.replace(hour=(day_end.hour - 1)%24)  # 1 hour before day ends
    duration_minutes = 3*60  # 3 hours
    expected_cost = 1 * Constants.PRIJS_PER_UUR_CHAUFFEUR + 2 * Constants.PRIJS_PER_UUR_CHAUFFEUR * (1 + Constants.EXTRA_AVOND)
    assert Cost.calculate_cost_time(start_time, duration_minutes) == pytest.approx(expected_cost)

    # Test part evening, part night, part day shift
    evening_end = Constants.TIJD_AVOND[1]
    start_time = evening_end.replace(hour=(evening_end.hour - 1)%24)  # 1 hour before evening ends
    duration_minutes = 8*60  # 8 hours
    expected_cost = (
        1 * Constants.PRIJS_PER_UUR_CHAUFFEUR * (1 + Constants.EXTRA_AVOND) +  # 1 hour evening
        6 * Constants.PRIJS_PER_UUR_CHAUFFEUR * (1 + Constants.EXTRA_NACHT) +  # 6 hours night
        1 * Constants.PRIJS_PER_UUR_CHAUFFEUR  # 1 hour day
    )
    assert Cost.calculate_cost_time(start_time, duration_minutes) == pytest.approx(expected_cost)

def test_calculate_cost_distance():
    distance_km = 100  # 100 kilometers
    expected_cost = 100 * Constants.PRIJS_PER_KM_BAKWAGEN
    assert Cost.calculate_cost_distance(distance_km, Auto_type.BAKWAGEN) == pytest.approx(expected_cost)

def test_no_overlap_between_periods():
    """
    Test to ensure there is no overlap between day, evening, and night times.
    """
    day_start, day_end = Constants.TIJD_DAG
    evening_start, evening_end = Constants.TIJD_AVOND
    night_start, night_end = Constants.TIJD_NACHT

    # Check if day and evening overlap
    assert day_end == evening_start, "Day and evening periods overlap"

    # Check if evening and night overlap
    assert evening_end == night_start, "Evening and night periods overlap"

    # Check if night and day overlap
    assert night_end == day_start, "Night and day periods overlap"

# Run the tests
if __name__ == "__main__":
    pytest.main()