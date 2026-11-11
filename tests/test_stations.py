from pybuoy import Buoy


def test_active_stations(buoy: Buoy) -> None:
    stations = buoy.stations.get_active()

    assert [s["id"] for s in stations] == ["21415", "32303", "41053", "44065"]
    assert stations[3] == {
        "id": "44065",
        "lat": "40.368",
        "lon": "-73.701",
        "elev": "0",
        "name": "New York Harbor Entrance - 15 NM SE of Breezy Point , NY",
        "owner": "NDBC",
        "pgm": "NDBC Meteorological/Ocean",
        "type": "buoy",
        "met": "y",
        "currents": "n",
        "waterquality": "n",
        "dart": "n",
    }


def test_stations_without_optional_attributes(buoy: Buoy) -> None:
    dart, tao, _, _ = buoy.stations.get_active()

    assert "elev" not in dart
    assert dart["dart"] == "y"
    assert tao["type"] == "tao"
    assert "met" not in tao
