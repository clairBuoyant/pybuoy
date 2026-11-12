from datetime import UTC, datetime, timedelta

import pytest
from conftest import FakeNoaa

from pybuoy import Buoy, Forecast, ParseError, RequestError, units
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


def test_request_asks_for_the_whole_forecast(buoy: Buoy, noaa: FakeNoaa) -> None:
    # NDFD reads begin and end as local time at the point, so none are sent
    # and the range is applied to its answer.
    buoy.forecasts.get(40.368, -73.701, START, END)

    params = noaa.calls[0]["params"]
    assert isinstance(params, dict)
    assert "begin" not in params
    assert "end" not in params
    assert (params["lat"], params["lon"]) == ("40.368", "-73.701")
    assert (params["product"], params["Unit"]) == ("time-series", "e")


def test_range_in_another_timezone_is_the_same_instant(buoy: Buoy) -> None:
    start = datetime.fromisoformat("2026-11-11T00:00:00-05:00")
    end = datetime.fromisoformat("2026-11-11T03:00:00-05:00")

    assert len(buoy.forecasts.get(40.368, -73.701, start, end)) == 4


def test_open_ended_range_returns_the_whole_forecast(buoy: Buoy) -> None:
    forecasts = buoy.forecasts.get(
        40.368,
        -73.701,
        datetime.min.replace(tzinfo=UTC),
        datetime.max.replace(tzinfo=UTC),
    )

    assert len(forecasts) == 4


def test_naive_datetimes_are_rejected(buoy: Buoy, noaa: FakeNoaa) -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        buoy.forecasts.get(40.368, -73.701, datetime(2026, 11, 11), END)  # noqa: DTZ001

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


def test_forecast_time_without_an_offset_raises_parse_error(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    noaa.bodies[noaa.forecast_url] = noaa.bodies[noaa.forecast_url].replace(
        "-05:00", ""
    )

    with pytest.raises(ParseError, match="offset"):
        buoy.forecasts.get(40.368, -73.701, START, END)


def test_forecast_time_out_of_range_raises_parse_error(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    # Year 1 at UTC+5 is before the earliest time Python can hold in UTC.
    noaa.bodies[noaa.forecast_url] = noaa.bodies[noaa.forecast_url].replace(
        "2026-11-11T00:00:00-05:00", "0001-01-01T00:00:00+05:00", 1
    )

    with pytest.raises(ParseError):
        buoy.forecasts.get(40.368, -73.701, START, END)


def test_unexpected_unit_raises_parse_error(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.bodies[noaa.forecast_url] = noaa.bodies[noaa.forecast_url].replace(
        'units="knots"', 'units="furlongs/fortnight"'
    )

    with pytest.raises(ParseError):
        buoy.forecasts.get(40.368, -73.701, START, END)


def test_parameters_pybuoy_does_not_model_are_ignored(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    temperature = (
        '<temperature type="hourly" units="Fahrenheit" time-layout="k-p1h-n61-1">'
        "<value>50</value><value>50</value><value>49</value><value>49</value>"
        "</temperature>"
    )
    noaa.bodies[noaa.forecast_url] = noaa.bodies[noaa.forecast_url].replace(
        "</parameters>", f"{temperature}</parameters>"
    )

    assert len(buoy.forecasts.get(40.368, -73.701, START, END)) == 4


def test_error_reported_by_noaa_raises_request_error(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    # NOAA answers an invalid point with status 200 and this body.
    noaa.bodies[noaa.forecast_url] = (
        '<error><h2>ERROR</h2><pre>Point with latitude "999" longitude "-73" '
        "is not on an NDFD grid</pre></error>"
    )

    with pytest.raises(RequestError, match="not on an NDFD grid") as raised:
        buoy.forecasts.get(999, -73, START, END)

    assert raised.value.status == 200


def test_xml_that_is_not_a_forecast_raises_parse_error() -> None:
    with pytest.raises(ParseError, match="html"):
        parse_dwml("<html><body>Maintenance</body></html>")


def test_start_after_end_is_rejected(buoy: Buoy, noaa: FakeNoaa) -> None:
    with pytest.raises(ValueError, match="start must not be after end"):
        buoy.forecasts.get(40.368, -73.701, END, START)

    assert noaa.calls == []
