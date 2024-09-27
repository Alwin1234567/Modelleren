import pytest
from source.structures import LocationToCoordinates

def test_location():
    testlocatie = LocationToCoordinates()
    print(testlocatie.adress())

# Run the test
if __name__ == "__main__":
    pytest.main()
