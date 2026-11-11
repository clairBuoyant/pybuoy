from datetime import UTC, datetime, timedelta

import pytest
from conftest import FakeNoaa

from pybuoy import Buoy, Forecast, ParseError, units
from pybuoy.forecasts import parse_dwml

# The fixture covers 00:00 to 03:00 at UTC-5.
START = datetime(2026, 11, 11, 5, tzinfo=UTC)
END = datetime(2026, 11, 11, 8, tzinfo=UTC)
HOUR = timedelta(hours=1)


def test_forecasts_are_merged_by_time_in_utc(buoy: Buoy) -> None:
    forecasts = buoy.forecasts.get(40.368, -73.701, START, END)

    assert [f.time for f in forecasts] == [START + n * HOUR for n in range(4)]


def test_forecast_values_are_converted_to_metric(buoy: Buoy) -> None:
    # The fixture reports 13 and 19 knots and 3 feet.
    assert buoy.forecasts.get(40.368, -73.701, START, END)[0] == Forecast(
        time=START,
        wind_direction=290.0,
        wind_speed=6.69,
        wind_gust=9.77,
        wave_height=0.91,
    )


def test_forecast_units() -> None:
    assert units(Forecast) == {
        "wind_direction": "degT",
        "wind_speed": "m/s",
        "wind_gust": "m/s",
        "wave_height": "m",
    }


def test_value_missing_from_a_shorter_time_layout_is_none(buoy: Buoy) -> None:
    last = buoy.forecasts.get(40.368, -73.701, START, END)[3]

    assert last.wave_height is None
    assert last.wind_direction == 300.0


def test_nil_value_is_none(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.bodies[noaa.forecast_url] = noaa.bodies[noaa.forecast_url].replace(
        "<value>290</value>", '<value xsi:nil="true"/>', 1
    )

    first, second, _, _ = buoy.forecasts.get(40.368, -73.701, START, END)

    assert first.wind_direction is None
    assert second.wind_direction == 290.0


def test_only_forecasts_inside_the_requested_range_are_returned(buoy: Buoy) -> None:
    forecasts = buoy.forecasts.get(40.368, -73.701, START + HOUR, END - HOUR)

    assert [f.time for f in forecasts] == [START + HOUR, START + 2 * HOUR]


def test_request_is_padded_because_ndfd_reads_local_time_without_offset(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    buoy.forecasts.get(40.368, -73.701, START, END)

    params = noaa.calls[0]["params"]
    assert isinstance(params, dict)
    assert params["begin"] == "2026-11-10T05:00:00"
    assert params["end"] == "2026-11-12T08:00:00"
    assert (params["lat"], params["lon"]) == ("40.368", "-73.701")
    assert (params["product"], params["Unit"]) == ("time-series", "e")


def test_range_in_another_timezone_is_the_same_instant(buoy: Buoy) -> None:
    start = datetime.fromisoformat("2026-11-11T00:00:00-05:00")
    end = datetime.fromisoformat("2026-11-11T03:00:00-05:00")

    assert len(buoy.forecasts.get(40.368, -73.701, start, end)) == 4


def test_naive_datetimes_are_rejected(buoy: Buoy, noaa: FakeNoaa) -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        buoy.forecasts.get(40.368, -73.701, datetime(2026, 11, 11), END)

    assert noaa.calls == []


def test_point_outside_the_ndfd_grid_has_no_forecasts() -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <dwml version="1.0">
      <data>
        <location><point latitude="0.00" longitude="0.00"/></location>
        <parameters applicable-location="point1"/>
      </data>
    </dwml>"""

    assert parse_dwml(xml) == []


def test_unexpected_unit_raises_parse_error(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.bodies[noaa.forecast_url] = noaa.bodies[noaa.forecast_url].replace(
        'units="knots"', 'units="furlongs/fortnight"'
    )

    with pytest.raises(ParseError):
        buoy.forecasts.get(40.368, -73.701, START, END)
