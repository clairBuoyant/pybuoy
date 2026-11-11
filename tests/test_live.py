"""Smoke tests against the real NOAA/NDBC services.

Deselected by default; run with ``pytest -m live``.
"""

from datetime import datetime, timedelta

import pytest

from pybuoy import Buoy
from pybuoy.observation import (
    ForecastObservation,
    MeteorologicalObservation,
    WaveSummaryObservation,
)

pytestmark = pytest.mark.live

STATION_ID = "44065"


def test_realtime_meteorological_data(buoy: Buoy) -> None:
    observations = buoy.realtime.get(STATION_ID)

    assert len(observations.reports) > 0
    assert all(type(o) is MeteorologicalObservation for o in observations)
    assert type(observations[0].datetime) is datetime


def test_realtime_wave_summary_data(buoy: Buoy) -> None:
    observations = buoy.realtime.get(STATION_ID, "spec")

    assert len(observations.reports) > 0
    assert all(type(o) is WaveSummaryObservation for o in observations)


def test_active_stations_include_the_example_station(buoy: Buoy) -> None:
    stations = buoy.stations.get_active()

    station = next(s for s in stations if s["id"] == STATION_ID)
    assert {"id", "lat", "lon", "name", "owner", "type"} <= station.keys()


def test_forecast_data(buoy: Buoy) -> None:
    start = datetime.now() + timedelta(days=1)
    end = start + timedelta(days=4)

    forecast = buoy.forecasts.get(40.368, -73.701, start.isoformat(), end.isoformat())

    assert len(forecast.reports) > 0
    assert all(type(f) is ForecastObservation for f in forecast)
