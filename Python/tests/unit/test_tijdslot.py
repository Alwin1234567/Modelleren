import pytest
from datetime import time
from source.structures import Tijdslot, Long_time

def test_init():
    # Test valid initialization
    start = Long_time(480)  # 480 minutes (8 hours)
    eind = Long_time(600)   # 600 minutes (10 hours)
    tijdslot = Tijdslot(start=start, eind=eind)
    assert tijdslot.starttijd.tijd == time(8, 0)
    assert tijdslot.eindtijd.tijd == time(10, 0)

    # Test invalid initialization (end time before start time)
    start = Long_time(600)  # 600 minutes (10 hours)
    eind = Long_time(480)   # 480 minutes (8 hours)
    with pytest.raises(ValueError):
        Tijdslot(start=start, eind=eind)

def test_is_in_tijdvak():
    start = Long_time(480)  # 480 minutes (8 hours)
    eind = Long_time(600)   # 600 minutes (10 hours)
    tijdslot = Tijdslot(start=start, eind=eind)
    
    # Test time within the slot
    tijd = Long_time(540)  # 540 minutes (9 hours)
    assert tijdslot.is_in_tijdvak(tijd) == True
    
    # Test time outside the slot
    tijd = Long_time(660)  # 660 minutes (11 hours)
    assert tijdslot.is_in_tijdvak(tijd) == False

def test_overlap():
    tijdslot1 = Tijdslot(start=Long_time(480), eind=Long_time(600))  # 8:00 to 10:00
    tijdslot2 = Tijdslot(start=Long_time(540), eind=Long_time(660))  # 9:00 to 11:00
    tijdslot3 = Tijdslot(start=Long_time(600), eind=Long_time(720))  # 10:00 to 12:00
    tijdslot4 = Tijdslot(start=Long_time(720), eind=Long_time(840))  # 12:00 to 14:00
    
    # Test overlapping slots
    assert tijdslot1.overlap(tijdslot2) == True
    assert tijdslot2.overlap(tijdslot3) == True
    assert tijdslot3.overlap(tijdslot4) == True
    
    # Test non-overlapping slots
    assert tijdslot1.overlap(tijdslot4) == False


if __name__ == '__main__':
    pytest.main()
