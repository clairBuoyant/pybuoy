"""NOAA National Digital Forecast Database (NDFD) point forecasts.

Service reference: https://graphical.weather.gov/xml/rest.php
"""

from collections import defaultdict
from dataclasses import fields
from datetime import UTC, datetime
from xml.etree import ElementTree

from pybuoy._http import Client
from pybuoy.errors import RequestError, _parser
from pybuoy.models import Forecast

_URL = "https://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php"
_XSI_NIL = "{http://www.w3.org/2001/XMLSchema-instance}nil"

# NDFD's metric output rounds wave height to whole metres, so request English
# units and convert them here.
_TO_METRIC = {"knots": 1852 / 3600, "feet": 0.3048, "degrees true": 1.0}


class Forecasts:
    """NOAA NDFD point forecasts, reached as ``Buoy().forecasts``."""

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

        NDFD forecasts about a week ahead, from now. A range that reaches
        outside that returns the part inside it, and a range wholly outside it,
        such as one in the past, returns an empty list. So does a point outside
        NDFD's coverage. A point NOAA rejects, such as an impossible latitude,
        raises ``RequestError``.
        """
        if start.utcoffset() is None or end.utcoffset() is None:
            raise ValueError("start and end must be timezone-aware")
        if start > end:
            raise ValueError("start must not be after end")

        # No begin or end is sent, so NDFD answers with its whole forecast. It
        # reads them as local time at the point, ignores one that carries a UTC
        # offset and answers nothing for an end past 2038, so the range is
        # applied to its answer instead.
        params: dict[str, str | float] = {
            "whichClient": "NDFDgen",
            "product": "time-series",
            "Unit": "e",
            "lat": lat,
            "lon": lon,
            "wspd": "wspd",
            "wdir": "wdir",
            "wgust": "wgust",
            "waveh": "waveh",
            "Submit": "Submit",
        }
        forecasts = parse_dwml(self._client.get(_URL, params))
        return [f for f in forecasts if start <= f.time <= end]


@_parser
def parse_dwml(xml: str) -> list[Forecast]:
    """Parse an NDFD time-series (DWML) response, converting values to metric.

    Each parameter lists its values against a named time layout, and layouts
    differ between parameters, so values are merged by time.
    """
    root = ElementTree.fromstring(xml)
    if root.tag == "error":
        # NOAA reports a rejected request in the body, with status 200.
        reason = root.findtext("pre", default="no reason given")
        raise RequestError(f"NOAA rejected the forecast request: {reason}", status=200)
    if root.tag != "dwml":
        raise ValueError(f"expected a <dwml> document, got <{root.tag}>")

    layouts = {
        layout.findtext("layout-key"): [
            _utc(time.text or "") for time in layout.iter("start-valid-time")
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
            factor = _TO_METRIC[series.get("units", "")]
            for time, value in zip(times, series.iter("value"), strict=True):
                by_time[time][name] = (
                    None
                    if value.get(_XSI_NIL) == "true"
                    else round(float(value.text or "") * factor, 2)
                )
    return [Forecast(time=time, **by_time[time]) for time in sorted(by_time)]


def _utc(text: str) -> datetime:
    moment = datetime.fromisoformat(text)
    if moment.utcoffset() is None:
        raise ValueError(f"forecast time {text!r} has no UTC offset")
    return moment.astimezone(UTC)
