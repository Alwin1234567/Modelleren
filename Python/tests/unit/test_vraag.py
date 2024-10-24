import pytest
from source.structures import Vraag
import warnings

def test_valid_initialization():
    vraag = Vraag([1, 2, 3, 4, 5, 6, 7])
    assert vraag.monday == 1
    assert vraag.sunday == 7

def test_non_integer_values():
    with pytest.raises(ValueError, match="All values must be integers."):
        Vraag([1, 2, 'three', 4, 5, 6, 7])

def test_more_than_seven_values():
    with pytest.raises(ValueError, match="There can be at most 7 values."):
        Vraag([1, 2, 3, 4, 5, 6, 7, 8])

def test_fewer_than_seven_values():
    with warnings.catch_warnings(record=True) as w:
        vraag = Vraag([1, 2, 3])
        assert len(w) == 1
        assert issubclass(w[-1].category, UserWarning)
        assert vraag.monday == 1
        assert vraag.sunday == 0  # Filled with 0

def test_properties():
    vraag = Vraag([1, 2, 3, 4, 5, 6, 7])
    assert vraag.monday == 1
    assert vraag.tuesday == 2
    assert vraag.wednesday == 3
    assert vraag.thursday == 4
    assert vraag.friday == 5
    assert vraag.saturday == 6
    assert vraag.sunday == 7

# Run the test
if __name__ == "__main__":
    pytest.main()
