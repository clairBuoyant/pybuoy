import pytest

from pybuoy import Buoy


# TODO: Mock Buoy endpoints
@pytest.fixture(scope="module")
def test_buoypy(station_id: str = "44065") -> Buoy:
    return Buoy(station_id=station_id)
