"""Smoke tests against the real NOAA/NDBC services.

Deselected by default; run with ``pytest -m live``.
"""

from datetime import UTC, datetime, timedelta

import pytest
import requests

from pybuoy import Buoy, Forecast, MeteorologicalObservation, WaveSummaryObservation

pytestmark = pytest.mark.live

STATION_ID = "44065"


def test_realtime_meteorological_data(buoy: Buoy) -> None:
    url = f"https://www.ndbc.noaa.gov/data/realtime2/{STATION_ID}.txt"
    raw = requests.get(url, timeout=10).text
    observations = buoy.realtime.get(STATION_ID)

    # Every line after the two header rows is one observation.
    assert len(observations) == len(raw.splitlines()) - 2
    assert all(type(o) is MeteorologicalObservation for o in observations)
    assert observations == sorted(observations, key=lambda o: o.time, reverse=True)


def test_realtime_wave_summary_data(buoy: Buoy) -> None:
    observations = buoy.realtime.get(STATION_ID, "spec")

    assert len(observations) > 0
    assert all(type(o) is WaveSummaryObservation for o in observations)
    # NDBC marks a missing direction with -99 here, which must not pass as data.
    directions = [o.dominant_wave_direction for o in observations]
    assert all(d is None or 0 <= d <= 360 for d in directions)


def test_active_stations_include_the_example_station(buoy: Buoy) -> None:
    stations = buoy.stations.get_active()

    station = next(s for s in stations if s.id == STATION_ID)
    assert (round(station.lat), round(station.lon)) == (40, -74)
    assert station.met is True


def test_forecast_data_stays_inside_the_requested_range(buoy: Buoy) -> None:
    start = datetime.now(UTC) + timedelta(days=1)
    end = start + timedelta(days=2)

    forecasts = buoy.forecasts.get(40.368, -73.701, start, end)

    assert len(forecasts) > 0
    assert all(type(f) is Forecast for f in forecasts)
    assert all(start <= f.time <= end for f in forecasts)
    assert forecasts[0].time - start < timedelta(hours=3)
    assert end - forecasts[-1].time < timedelta(hours=6)


def test_forecast_for_a_point_on_land_has_wind_but_no_waves(buoy: Buoy) -> None:
    start = datetime.now(UTC)

    forecasts = buoy.forecasts.get(39.74, -104.99, start, start + timedelta(days=1))

    assert len(forecasts) > 0
    assert all(f.wave_height is None for f in forecasts)
    assert any(f.wind_speed is not None for f in forecasts)


def test_forecast_with_an_open_end_reaches_the_end_of_noaa_data(buoy: Buoy) -> None:
    start = datetime.now(UTC)

    forecasts = buoy.forecasts.get(
        40.368, -73.701, start, datetime.max.replace(tzinfo=UTC)
    )

    assert forecasts[-1].time - start > timedelta(days=5)
