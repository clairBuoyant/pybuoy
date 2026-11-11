from datetime import datetime, timedelta, timezone

from pybuoy import Buoy
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


def test_forecast_request_parameters(buoy: Buoy, noaa: list[dict]) -> None:
    buoy.forecasts.get(40.368, -73.701, START, END)

    params = noaa[0]["params"]
    assert params["lat"] == 40.368
    assert params["lon"] == -73.701
    assert params["begin"] == START
    assert params["end"] == END
    assert params["product"] == "time-series"
