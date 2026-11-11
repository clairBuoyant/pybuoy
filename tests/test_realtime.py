from datetime import datetime

import pytest
from conftest import FakeNoaa

from pybuoy import Buoy
from pybuoy.exceptions import NDBCException
from pybuoy.observation import MeteorologicalObservation, WaveSummaryObservation


def test_meteorological_observations_are_parsed_newest_first(buoy: Buoy) -> None:
    observations = buoy.realtime.get("44065")

    assert [type(o) for o in observations] == [MeteorologicalObservation] * 3
    assert [o.datetime for o in observations] == [
        datetime(2026, 11, 11, 1, 10),
        datetime(2026, 11, 11, 1, 0),
        datetime(2026, 11, 11, 0, 50),
    ]


def test_meteorological_values(buoy: Buoy) -> None:
    first, second, third = buoy.realtime.get("44065")

    assert first.wind_direction.value == 230.0
    assert first.wind_speed.value == 9.0
    assert first.wind_gust.value == 10.0
    assert first.wave_height.value == 0.7
    assert first.average_wave_period.value == 3.6
    assert first.wave_direction.value == 109.0
    assert first.sea_level_pressure.value == 1012.6
    assert first.air_temperature.value == 15.6
    assert first.water_temperature.value == 15.8
    assert first.dewpoint_temperature.value == 9.4
    assert second.pressure_tendency.value == 1.0
    assert third.dominant_wave_period.value == 11.0


def test_meteorological_missing_values_are_none(buoy: Buoy) -> None:
    first, second, _ = buoy.realtime.get("44065")

    assert first.dominant_wave_period.value is None
    assert first.visibility.value is None
    assert first.pressure_tendency.value is None
    assert first.tide.value is None
    assert second.wave_height.value is None


def test_meteorological_units(buoy: Buoy) -> None:
    first = buoy.realtime.get("44065")[0]

    assert first.wind_speed.unit == "m/s"
    assert first.wave_height.unit == "m"
    assert first.sea_level_pressure.unit == "hPa"


def test_wave_summary_values(buoy: Buoy) -> None:
    first, second, third = buoy.realtime.get("44065", "spec")

    assert type(first) is WaveSummaryObservation
    assert first.datetime == datetime(2026, 11, 11, 1, 10)
    assert first.significant_wave_height.value == 0.7
    assert first.swell_height.value == 0.3
    assert first.swell_period.value == 10.8
    assert first.wind_wave_height.value == 0.6
    assert first.wind_wave_period.value == 3.6
    assert first.swell_direction.value == "ESE"
    assert first.wind_wave_direction.value == "SSW"
    assert first.average_wave_period.value == 3.6
    assert first.dominant_wave_direction.value == 109.0
    assert second.steepness.value == "VERY_STEEP"
    assert third.steepness.value == "STEEP"


def test_wave_summary_missing_values_are_none(buoy: Buoy) -> None:
    first, second, third = buoy.realtime.get("44065", "spec")

    assert first.steepness.value is None
    assert second.wind_wave_direction.value is None
    assert third.swell_period.value is None
    assert third.swell_direction.value is None


def test_unknown_station_raises_with_a_message(
    buoy: Buoy, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(NDBCException, match=r"realtime2/ZZZZZ\.txt"):
        buoy.realtime.get("ZZZZZ")

    assert capsys.readouterr().out == ""


def test_requests_have_a_timeout(buoy: Buoy, noaa: FakeNoaa) -> None:
    buoy.realtime.get("44065")

    assert noaa.calls[0]["timeout"] == 10


def test_station_id_is_required(buoy: Buoy) -> None:
    with pytest.raises(ValueError, match="station_id"):
        buoy.realtime.get("")


@pytest.mark.parametrize(
    "dataset", ["data_spec", "ocean", "supl", "swdir", "swdir2", "swr1", "swr2"]
)
def test_datasets_without_a_parser_are_rejected(
    buoy: Buoy, noaa: FakeNoaa, dataset: str
) -> None:
    with pytest.raises(ValueError, match="spec, txt"):
        buoy.realtime.get("44065", dataset)  # type: ignore[call-overload]

    assert noaa.calls == []
