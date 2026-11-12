from datetime import UTC, datetime
from typing import Any

import pytest
from conftest import FakeNoaa

from pybuoy import (
    Buoy,
    MeteorologicalObservation,
    ParseError,
    WaveSummaryObservation,
    units,
)
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
    _, second, third, _ = buoy.realtime.get("44065", "spec")

    assert second.steepness == "VERY_STEEP"
    assert second.wind_wave_direction is None
    assert third.steepness == "STEEP"
    assert third.swell_period is None
    assert third.swell_direction is None


def test_minus_99_wave_direction_is_none(buoy: Buoy) -> None:
    # In the last row of the fixture -99 marks a missing direction, not MM.
    last = buoy.realtime.get("44065", "spec")[-1]

    assert last.dominant_wave_direction is None
    assert last.average_wave_period == 3.6


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


def test_malformed_rows_raise_parse_error(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.bodies[noaa.realtime_url] += "2026 11 11 00 40 230\n"

    with pytest.raises(ParseError):
        buoy.realtime.get("44065")


@pytest.mark.parametrize(
    "body",
    [
        "<html>Service unavailable</html>",
        "<html>\n<body>Service unavailable</body></html>",
        "#STN  LAT LON\n#text deg deg\n",
    ],
)
def test_a_body_that_is_not_a_realtime_file_raises_parse_error(body: str) -> None:
    with pytest.raises(ParseError):
        parse_realtime(body, MeteorologicalObservation)


@pytest.mark.parametrize("station_id", ["", "44065.txt", "../activestations"])
def test_station_id_must_be_letters_and_digits(
    buoy: Buoy, noaa: FakeNoaa, station_id: str
) -> None:
    with pytest.raises(ValueError, match="station_id"):
        buoy.realtime.get(station_id)

    assert noaa.calls == []


def test_numeric_station_id_may_be_an_int(buoy: Buoy) -> None:
    assert buoy.realtime.get(44065) == buoy.realtime.get("44065")


def test_station_id_is_upper_cased_because_ndbc_paths_are_case_sensitive(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    url = "https://www.ndbc.noaa.gov/data/realtime2/BURL1.txt"
    noaa.bodies[url] = noaa.bodies[noaa.realtime_url]

    assert len(buoy.realtime.get("burl1")) == 3
    assert noaa.calls[0]["url"] == url


@pytest.mark.parametrize("dataset", ["ocean", "swdir", "TXT"])
def test_datasets_without_a_parser_are_rejected(
    buoy: Buoy, noaa: FakeNoaa, dataset: str
) -> None:
    get: Any = buoy.realtime.get  # the type checker rejects these datasets

    with pytest.raises(ValueError, match="txt, spec"):
        get("44065", dataset)

    assert noaa.calls == []
