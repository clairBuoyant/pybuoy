from random import randrange

from pybuoy import Buoy
from pybuoy.mixins.parser import XmlToDict


def test_activestations_from_xml(test_buoypy: Buoy):
    response = test_buoypy.stations.get_active()

    random_station = response[randrange(len(response))]

    assert isinstance(random_station, XmlToDict)
    assert "id" in random_station
    assert "lat" in random_station
    assert "lon" in random_station
    assert "name" in random_station
    assert "owner" in random_station
    assert "type" in random_station
    assert "met" in random_station
    assert "currents" in random_station
    assert "waterquality" in random_station
