"""NDBC active stations."""

from xml.etree import ElementTree

from pybuoy._http import Client
from pybuoy.errors import _parser
from pybuoy.models import Station

_URL = "https://www.ndbc.noaa.gov/activestations.xml"


class Stations:
    def __init__(self, client: Client) -> None:
        self._client = client

    def get_active(self) -> list[Station]:
        """Get every station NDBC currently lists as active."""
        return parse_active_stations(self._client.get(_URL))


@_parser
def parse_active_stations(xml: str) -> list[Station]:
    """Parse NDBC's ``activestations.xml``."""
    root = ElementTree.fromstring(xml)
    if root.tag != "stations":
        raise ValueError(f"expected a <stations> document, got <{root.tag}>")

    return [
        Station(
            id=station.attrib["id"],
            name=station.attrib["name"],
            lat=float(station.attrib["lat"]),
            lon=float(station.attrib["lon"]),
            owner=station.attrib["owner"],
            program=station.attrib["pgm"],
            type=station.attrib["type"],
            elevation=float(station.attrib["elev"])
            if "elev" in station.attrib
            else None,
            met=station.get("met") == "y",
            currents=station.get("currents") == "y",
            water_quality=station.get("waterquality") == "y",
            dart=station.get("dart") == "y",
        )
        for station in root.iter("station")
    ]
