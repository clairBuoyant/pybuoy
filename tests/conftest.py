import pytest

from pybuoy import Buoy


# TODO: Mock Buoy endpoints
@pytest.fixture(scope="module")
def test_pybuoy() -> Buoy:
    return Buoy()
