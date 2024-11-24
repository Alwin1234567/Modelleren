import pytest
from source.flow import Create_locations, store_results

def test_store_results():
    # Arrange
    create_locations = Create_locations()
    hubs = create_locations.hubs

    # Act
    store_results(hubs)

    # Assert

if __name__ == '__main__':
    pytest.main()
