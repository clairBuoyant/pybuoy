from datetime import UTC, datetime

import pytest
from conftest import FakeNoaa

from pybuoy import Buoy, MeteorologicalObservation, WaveSummaryObservation, units
from pybuoy.exceptions import NDBCException
from pybuoy.realtime import parse_realtime


def test_meteorological_observations_are_newest_first_in_utc(buoy: Buoy) -> None:
    observations = buoy.realtime.get("44065")

    assert [o.time for o in observations] == [
        datetime(2026, 11, 11, 1, 10, tzinfo=UTC),
        datetime(2026, 11, 11, 1, 0, tzinfo=UTC),
        datetime(2026, 11, 11, 0, 50, tzinfo=UTC),
    ]


def test_meteorological_observation(buoy: Buoy) -> None:
    assert buoy.realtime.get("44065")[0] == MeteorologicalObservation(
        time=datetime(2026, 11, 11, 1, 10, tzinfo=UTC),
        wind_direction=230.0,
        wind_speed=9.0,
        wind_gust=10.0,
        wave_height=0.7,
        dominant_wave_period=None,
        average_wave_period=3.6,
        wave_direction=109.0,
        sea_level_pressure=1012.6,
        air_temperature=15.6,
        water_temperature=15.8,
        dewpoint_temperature=9.4,
        visibility=None,
        pressure_tendency=None,
        tide=None,
    )


def test_meteorological_values_that_vary_between_rows(buoy: Buoy) -> None:
    _, second, third = buoy.realtime.get("44065")

    assert second.wave_height is None
    assert second.pressure_tendency == 1.0
    assert third.dominant_wave_period == 11.0


def test_wave_summary_observation(buoy: Buoy) -> None:
    assert buoy.realtime.get("44065", "spec")[0] == WaveSummaryObservation(
        time=datetime(2026, 11, 11, 1, 10, tzinfo=UTC),
        significant_wave_height=0.7,
        swell_height=0.3,
        swell_period=10.8,
        wind_wave_height=0.6,
        wind_wave_period=3.6,
        swell_direction="ESE",
        wind_wave_direction="SSW",
        steepness=None,
        average_wave_period=3.6,
        dominant_wave_direction=109.0,
    )


def test_wave_summary_values_that_vary_between_rows(buoy: Buoy) -> None:
    _, second, third = buoy.realtime.get("44065", "spec")

    assert second.steepness == "VERY_STEEP"
    assert second.wind_wave_direction is None
    assert third.steepness == "STEEP"
    assert third.swell_period is None
    assert third.swell_direction is None


def test_units_are_declared_once_per_model() -> None:
    assert units(MeteorologicalObservation) == {
        "wind_direction": "degT",
        "wind_speed": "m/s",
        "wind_gust": "m/s",
        "wave_height": "m",
        "dominant_wave_period": "sec",
        "average_wave_period": "sec",
        "wave_direction": "degT",
        "sea_level_pressure": "hPa",
        "air_temperature": "degC",
        "water_temperature": "degC",
        "dewpoint_temperature": "degC",
        "visibility": "nmi",
        "pressure_tendency": "hPa",
        "tide": "ft",
    }
    assert "swell_direction" not in units(WaveSummaryObservation)


def test_unknown_columns_are_ignored_and_absent_columns_are_none() -> None:
    body = (
        "#YY  MM DD hh mm WSPD  NEW\n"
        "#yr  mo dy hr mn  m/s    -\n"
        "2026 11 11 01 10  9.0  1.5\n"
    )

    assert parse_realtime(body, MeteorologicalObservation) == [
        MeteorologicalObservation(
            time=datetime(2026, 11, 11, 1, 10, tzinfo=UTC), wind_speed=9.0
        )
    ]


def test_a_response_without_rows_is_empty() -> None:
    body = "#YY  MM DD hh mm WSPD\n#yr  mo dy hr mn  m/s\n"

    assert parse_realtime(body, MeteorologicalObservation) == []


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


@pytest.mark.parametrize("dataset", ["ocean", "swdir", "TXT"])
def test_datasets_without_a_parser_are_rejected(
    buoy: Buoy, noaa: FakeNoaa, dataset: str
) -> None:
    with pytest.raises(ValueError, match="txt, spec"):
        buoy.realtime.get("44065", dataset)  # type: ignore[call-overload]

    assert noaa.calls == []
