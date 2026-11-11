"""NOAA National Digital Forecast Database (NDFD) point forecasts.

Service reference: https://graphical.weather.gov/xml/rest.php
"""

from collections import defaultdict
from dataclasses import fields
from datetime import UTC, datetime, timedelta
from xml.etree import ElementTree

from pybuoy._http import Client
from pybuoy.errors import parser
from pybuoy.models import Forecast

URL = "https://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php"
XSI_NIL = "{http://www.w3.org/2001/XMLSchema-instance}nil"

# NDFD's metric output rounds wave height to whole metres, so request English
# units and convert them here.
TO_METRIC = {"knots": 1852 / 3600, "feet": 0.3048, "degrees true": 1.0}

# NDFD reads begin/end as local time at the point and ignores any value that
# carries a UTC offset. Ask for a day either side, then keep the exact range.
PADDING = timedelta(days=1)


class Forecasts:
    def __init__(self, client: Client) -> None:
        self._client = client

    def get(
        self, lat: float, lon: float, start: datetime, end: datetime
    ) -> list[Forecast]:
        """Get the wind and wave forecast for a point, oldest first.

        Args:
            lat: latitude in decimal degrees.
            lon: longitude in decimal degrees.
            start: earliest forecast time wanted; must be timezone-aware.
            end: latest forecast time wanted; must be timezone-aware.

        A point outside NDFD's coverage has no forecasts.
        """
        if start.utcoffset() is None or end.utcoffset() is None:
            raise ValueError("start and end must be timezone-aware")

        params: dict[str, str | float] = {
            "whichClient": "NDFDgen",
            "product": "time-series",
            "Unit": "e",
            "lat": lat,
            "lon": lon,
            "begin": _ndfd_time(start - PADDING),
            "end": _ndfd_time(end + PADDING),
            "wspd": "wspd",
            "wdir": "wdir",
            "wgust": "wgust",
            "waveh": "waveh",
            "Submit": "Submit",
        }
        forecasts = parse_dwml(self._client.get(URL, params))
        return [f for f in forecasts if start <= f.time <= end]


@parser
def parse_dwml(xml: str) -> list[Forecast]:
    """Parse an NDFD time-series (DWML) response, converting values to metric.

    Each parameter lists its values against a named time layout, and layouts
    differ between parameters, so values are merged by time.
    """
    root = ElementTree.fromstring(xml)
    layouts = {
        layout.findtext("layout-key"): [
            datetime.fromisoformat(time.text or "").astimezone(UTC)
            for time in layout.iter("start-valid-time")
        ]
        for layout in root.iter("time-layout")
    }
    names = {f.metadata["source"]: f.name for f in fields(Forecast) if f.metadata}

    by_time: defaultdict[datetime, dict[str, float | None]] = defaultdict(dict)
    for parameter in root.iterfind("data/parameters/*"):
        times = layouts[parameter.get("time-layout")]
        # Wave series are nested one level down, inside <water-state>.
        for series in parameter.findall("waves") or [parameter]:
            name = names.get(f"{series.tag}/{series.get('type')}")
            if name is None:
                continue
            factor = TO_METRIC[series.get("units", "")]
            for time, value in zip(times, series.iter("value"), strict=True):
                by_time[time][name] = (
                    None
                    if value.get(XSI_NIL) == "true"
                    else round(float(value.text or "") * factor, 2)
                )
    return [Forecast(time=time, **by_time[time]) for time in sorted(by_time)]


def _ndfd_time(moment: datetime) -> str:
    return moment.astimezone(UTC).replace(tzinfo=None).isoformat(timespec="seconds")
