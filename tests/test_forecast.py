from datetime import datetime, timedelta, timezone

import pytest
from conftest import FakeNoaa

from pybuoy import Buoy
from pybuoy.exceptions import NOAAException
from pybuoy.observation import ForecastObservation

EST = timezone(timedelta(hours=-5))
START = "2026-11-11T00:00:00"
END = "2026-11-11T03:00:00"


def test_forecast_is_merged_by_timestamp(buoy: Buoy) -> None:
    forecast = buoy.forecasts.get(40.368, -73.701, START, END)

    assert [type(f) for f in forecast] == [ForecastObservation] * 4
    assert [f.datetime for f in forecast] == [
        datetime(2026, 11, 11, hour, tzinfo=EST) for hour in range(4)
    ]


def test_forecast_values(buoy: Buoy) -> None:
    first, _, _, last = buoy.forecasts.get(40.368, -73.701, START, END)

    assert first.wind_speed.value == 13.0
    assert first.wind_gust.value == 19.0
    assert first.wind_direction.value == 290.0
    assert first.wave_height.value == 3.0
    assert last.wind_direction.value == 300.0


def test_forecast_value_missing_from_a_shorter_time_layout_is_none(buoy: Buoy) -> None:
    last = buoy.forecasts.get(40.368, -73.701, START, END)[3]

    assert last.wave_height.value is None
    assert last.wind_speed.value == 13.0


def test_forecast_request_parameters(buoy: Buoy, noaa: FakeNoaa) -> None:
    buoy.forecasts.get(40.368, -73.701, START, END)

    params = noaa.calls[0]["params"]
    assert isinstance(params, dict)
    assert params["lat"] == 40.368
    assert params["lon"] == -73.701
    assert params["begin"] == START
    assert params["end"] == END
    assert params["product"] == "time-series"


def test_forecast_dates_are_sent_without_microseconds(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    # NDFD ignores a begin/end it cannot parse and returns its full range.
    buoy.forecasts.get(
        40.368, -73.701, "2026-11-11T00:00:00.123456", "2026-11-11T03:00:00.654321"
    )

    params = noaa.calls[0]["params"]
    assert isinstance(params, dict)
    assert params["begin"] == "2026-11-11T00:00:00"
    assert params["end"] == "2026-11-11T03:00:00"


def test_forecast_nil_value_is_none(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.bodies[noaa.forecast_url] = noaa.bodies[noaa.forecast_url].replace(
        "<value>290</value>", '<value xsi:nil="true"/>', 1
    )

    first, second, _, _ = buoy.forecasts.get(40.368, -73.701, START, END)

    assert first.wind_direction.value is None
    assert second.wind_direction.value == 290.0


def test_forecast_has_a_length(buoy: Buoy) -> None:
    assert len(buoy.forecasts.get(40.368, -73.701, START, END)) == 4


def test_forecast_for_a_point_without_waves(buoy: Buoy, noaa: FakeNoaa) -> None:
    # NOAA leaves out the wave parameter for points on land.
    body = noaa.bodies[noaa.forecast_url]
    waves = body[body.index("<water-state") : body.index("</water-state>")]
    noaa.bodies[noaa.forecast_url] = body.replace(waves + "</water-state>", "")

    forecast = buoy.forecasts.get(39.74, -104.99, START, END)

    assert len(forecast) == 4
    assert forecast[0].wind_speed.value == 13.0
    assert forecast[0].wind_direction.value == 290.0
    assert forecast[0].wave_height.value is None


def test_forecast_for_a_point_with_only_wind_direction(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    body = noaa.bodies[noaa.forecast_url]
    for tag in ("water-state", "wind-speed", "wind-speed"):
        start, end = body.index(f"<{tag}"), body.index(f"</{tag}>")
        body = body[:start] + body[end + len(f"</{tag}>") :]
    noaa.bodies[noaa.forecast_url] = body

    forecast = buoy.forecasts.get(39.74, -104.99, START, END)

    assert forecast[0].wind_direction.value == 290.0
    assert forecast[0].wind_speed.value is None


def test_error_reported_by_noaa_raises_with_its_message(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    # NOAA answers an invalid point with status 200 and this body.
    noaa.bodies[noaa.forecast_url] = (
        '<error><h2>ERROR</h2><pre>Point with latitude "999" longitude "-73" '
        "is not on an NDFD grid</pre></error>"
    )

    with pytest.raises(NOAAException, match="not on an NDFD grid"):
        buoy.forecasts.get(999, -73, START, END)


def test_forecast_dates_with_an_offset_select_the_exact_range(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    # NDFD ignores a date that carries an offset, so it is sent as a naive
    # date a day wider and the answer is cut to the instants asked for.
    forecast = buoy.forecasts.get(
        40.368, -73.701, "2026-11-11T05:00:00+00:00", "2026-11-11T08:00:00+01:00"
    )

    params = noaa.calls[0]["params"]
    assert isinstance(params, dict)
    assert params["begin"] == "2026-11-10T05:00:00"
    assert params["end"] == "2026-11-12T07:00:00"
    assert [f.datetime for f in forecast] == [
        datetime(2026, 11, 11, hour, tzinfo=EST) for hour in range(3)
    ]
