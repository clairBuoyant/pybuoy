from random import randrange

from pybuoy import Buoy
from pybuoy.mixins.parser import XmlToDict

example_station_id = "44065"


def find_buoy(buoys: list[XmlToDict], station_id: str):
    return next((buoy for buoy in buoys if buoy.get("id", None) == station_id), None)


def test_activestations_from_xml(test_pybuoy: Buoy):
    response = test_pybuoy.stations.get_active()

    random_station = response[randrange(len(response))]

    assert isinstance(random_station, XmlToDict)
    assert "id" in random_station
    assert "lat" in random_station
    assert "lon" in random_station
    assert "name" in random_station
    assert "owner" in random_station
    assert "type" in random_station

    is_type_tao = True if random_station.get("type", None) == "tao" else False
    if not is_type_tao:
        assert "met" in random_station
        assert "currents" in random_station
        assert "waterquality" in random_station
    else:
        assert random_station.get("type") == "tao"


def test_rockaway_beach_buoy(test_pybuoy: Buoy):
    response = test_pybuoy.stations.get_active()

    rockaway_buoy = find_buoy(response, example_station_id)
    assert isinstance(rockaway_buoy, XmlToDict)

    assert "id" in rockaway_buoy
    assert "lat" in rockaway_buoy
    assert "lon" in rockaway_buoy
    assert "name" in rockaway_buoy
    assert "owner" in rockaway_buoy
    assert "type" in rockaway_buoy
    assert "met" in rockaway_buoy
    assert "currents" in rockaway_buoy
    assert "waterquality" in rockaway_buoy

    expected_lat = "40.369"
    expected_lon = "-73.703"
    expected_name = "New York Harbor Entrance - 15 NM SE of Breezy Point , NY"
    assert rockaway_buoy.get("lat") == expected_lat
    assert rockaway_buoy.get("lon") == expected_lon
    assert rockaway_buoy.get("name") == expected_name
