from pybuoy import Buoy, Station


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
