import pytest
from conftest import FakeNoaa

from pybuoy import Buoy, ParseError, Station


def test_active_stations(buoy: Buoy) -> None:
    stations = buoy.stations.get_active()

    assert [s.id for s in stations] == ["21415", "32303", "41053", "44065"]
    assert stations[3] == Station(
        id="44065",
        name="New York Harbor Entrance - 15 NM SE of Breezy Point , NY",
        lat=40.368,
        lon=-73.701,
        owner="NDBC",
        program="NDBC Meteorological/Ocean",
        type="buoy",
        elevation=0.0,
        met=True,
        currents=False,
        water_quality=False,
        dart=False,
    )


def test_station_with_every_sensor_flag_set(buoy: Buoy) -> None:
    station = buoy.stations.get_active()[2]

    assert (station.met, station.currents, station.water_quality) == (True, True, True)


def test_stations_without_optional_attributes(buoy: Buoy) -> None:
    dart, tao, _, _ = buoy.stations.get_active()

    assert dart.elevation is None
    assert dart.dart is True
    assert tao.type == "tao"
    assert (tao.met, tao.currents, tao.water_quality, tao.dart) == (
        False,
        False,
        False,
        False,
    )


def test_station_names_are_read_as_utf_8(buoy: Buoy, noaa: FakeNoaa) -> None:
    # NDBC declares no charset for this file, which requests reads as Latin-1.
    noaa.bodies[noaa.stations_url] = noaa.bodies[noaa.stations_url].replace(
        "5N 95W", "Añasco, PR"
    )

    assert buoy.stations.get_active()[1].name == "Añasco, PR"


def test_malformed_xml_raises_parse_error(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.bodies[noaa.stations_url] = "<stations><station"

    with pytest.raises(ParseError):
        buoy.stations.get_active()


def test_station_without_a_required_attribute_raises_parse_error(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    noaa.bodies[noaa.stations_url] = '<stations><station id="44065"/></stations>'

    with pytest.raises(ParseError):
        buoy.stations.get_active()


def test_xml_that_is_not_a_station_list_raises_parse_error(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    noaa.bodies[noaa.stations_url] = "<html><body>Maintenance</body></html>"

    with pytest.raises(ParseError, match="html"):
        buoy.stations.get_active()
