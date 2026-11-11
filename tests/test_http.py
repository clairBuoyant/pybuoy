from importlib.metadata import version

import pytest
import requests
from conftest import FakeNoaa

import pybuoy
from pybuoy import Buoy, PybuoyError, RequestError, StationNotFoundError


def test_requests_time_out_after_ten_seconds_by_default(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    buoy.stations.get_active()

    assert noaa.calls[0]["timeout"] == 10.0


def test_timeout_is_configurable(session: requests.Session, noaa: FakeNoaa) -> None:
    Buoy(timeout=3.0, session=session).stations.get_active()

    assert noaa.calls[0]["timeout"] == 3.0


def test_error_status_raises_request_error(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.status = 503

    with pytest.raises(RequestError, match="503") as raised:
        buoy.stations.get_active()

    assert raised.value.status == 503


def test_transport_failure_raises_request_error(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.error = requests.ConnectionError("connection refused")

    with pytest.raises(RequestError, match="connection refused") as raised:
        buoy.stations.get_active()

    assert raised.value.status is None
    assert raised.value.__cause__ is noaa.error


def test_unknown_station_raises_station_not_found(buoy: Buoy) -> None:
    with pytest.raises(StationNotFoundError, match="'txt' data for station 'ZZZZZ'"):
        buoy.realtime.get("ZZZZZ")


def test_other_realtime_failures_are_request_errors(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.status = 500

    with pytest.raises(RequestError, match="500"):
        buoy.realtime.get("44065")


@pytest.mark.parametrize("error", [RequestError, StationNotFoundError])
def test_every_error_is_a_pybuoy_error(error: type[Exception]) -> None:
    assert issubclass(error, PybuoyError)


def test_version_comes_from_the_installed_package() -> None:
    assert pybuoy.__version__ == version("pybuoy")
