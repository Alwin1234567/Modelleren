import pytest
from datetime import time
from source.structures import Long_time

def test_init():
    # Test valid initialization with float
    lt = Long_time(2190)  # 2190 minutes (36 hours and 30 minutes)
    assert lt.tijd == time(12, 30)
    assert lt.dag == 1

    # Test valid initialization with time
    lt = Long_time(time(8, 0), dag=2)
    assert lt.tijd == time(8, 0)
    assert lt.dag == 2
    
    with pytest.warns(RuntimeWarning):
        lt = Long_time(2190, dag=1)

def test_float_conversion():
    lt = Long_time(2190)  # 2190 minutes (36 hours and 30 minutes)
    assert float(lt) == 2190

    lt = Long_time(time(8, 0), dag=2)
    assert float(lt) == 2880 + 480  # 2 days (2880 minutes) + 8 hours (480 minutes)

def test_gt():
    lt1 = Long_time(2190)
    lt2 = Long_time(1440)
    assert lt1 > lt2
    assert not (lt2 > lt1)

def test_ge():
    lt1 = Long_time(2190)
    lt2 = Long_time(2190)
    lt3 = Long_time(1440)
    assert lt1 >= lt2
    assert lt1 >= lt3
    assert not (lt3 >= lt1)

def test_eq():
    lt1 = Long_time(2190)
    lt2 = Long_time(2190)
    lt3 = Long_time(1440)
    assert lt1 == lt2
    assert not (lt1 == lt3)

def test_lt():
    lt1 = Long_time(1440)
    lt2 = Long_time(2190)
    assert lt1 < lt2
    assert not (lt2 < lt1)

def test_le():
    lt1 = Long_time(2190)
    lt2 = Long_time(2190)
    lt3 = Long_time(1440)
    assert lt3 <= lt1
    assert lt1 <= lt2
    assert not (lt1 <= lt3)

def test_add():
    lt1 = Long_time(2190)  # 2190 minutes (36 hours and 30 minutes)
    lt2 = Long_time(1440)  # 1440 minutes (24 hours)

    # Add float
    lt3 = lt1 + 150  # Add 150 minutes (2 hours and 30 minutes)
    assert float(lt3) == 2340

    # Add time
    lt4 = lt1 + time(1, 30)  # Add 1 hour and 30 minutes (90 minutes)
    assert float(lt4) == 2280

    # Add Long_time
    lt5 = lt1 + lt2
    assert float(lt5) == 3630

    lt6 = lt1 + 150 + time(1, 30) + lt2
    assert float(lt6) == 3870

    # Test invalid addition
    with pytest.raises(TypeError):
        lt1 + "invalid"

def test_sub():
    lt1 = Long_time(2190)  # 2190 minutes (36 hours and 30 minutes)
    lt2 = Long_time(1440)  # 1440 minutes (24 hours)

    # Subtract float
    lt3 = lt1 - 150  # Subtract 150 minutes (2 hours and 30 minutes)
    assert float(lt3) == 2040

    # Subtract time
    lt4 = lt1 - time(1, 30)  # Subtract 1 hour and 30 minutes (90 minutes)
    assert float(lt4) == 2100

    # Subtract Long_time
    lt5 = lt1 - lt2
    assert float(lt5) == 750

    lt6 = lt1 - 150 - time(1, 30) - lt2
    assert float(lt6) == 510

    # Test invalid subtraction
    with pytest.raises(TypeError):
        lt1 - "invalid"

def test_difference():
    lt1 = Long_time(2190)  # 2190 minutes (36 hours and 30 minutes)
    lt2 = Long_time(1440)  # 1440 minutes (24 hours)
    lt3 = Long_time(2340)  # 2340 minutes (39 hours)

    # Test difference
    assert lt1.difference(lt2) == 750  # 2190 - 1440 = 750 minutes
    assert lt2.difference(lt1) == 750  # 1440 - 2190 = 750 minutes (absolute value)
    assert lt3.difference(lt1) == 150  # 2340 - 2190 = 150 minutes

if __name__ == '__main__':
    pytest.main()
