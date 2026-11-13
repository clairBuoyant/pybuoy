from collections import defaultdict
from datetime import UTC, timedelta
from datetime import datetime as dt
from json import loads

import lxml.etree as ET  # type: ignore

from pybuoy.api.base import ApiBase
from pybuoy.const import API_PATH, Endpoints
from pybuoy.exceptions import NOAAException
from pybuoy.observation import ForecastObservation, ForecastObservations
from pybuoy.unit_mappings import NO_NUMERIC_VALUE

# NDFD reads begin/end as local time at the point and ignores a date that
# carries a UTC offset. Such a date is sent without its offset and a day wider,
# and the answer is cut to the instants asked for.
_PADDING = timedelta(days=1)


class Forecasts(ApiBase):
    # https://graphical.weather.gov/xml/rest.php
    def get(self, lat: float, lon: float, start_date: str, end_date: str):
        start, end = dt.fromisoformat(start_date), dt.fromisoformat(end_date)
        dwml_data = self.forecast_by_lat_lon(
            lat=lat,
            lon=lon,
            start_date=_without_offset(start, -_PADDING),
            end_date=_without_offset(end, _PADDING),
        )
        grouped = self.__group_parameters_by_time(dwml_data["data"]["parameters"])
        times = {key: dt.fromisoformat(key) for key in grouped}

        return ForecastObservations(
            observations=[
                ForecastObservation(grouped[key], time)
                for key, time in times.items()
                if (start.tzinfo is None or start <= time)
                and (end.tzinfo is None or time <= end)
            ],
            repr_limit=10,
        )

    def forecast_by_lat_lon(
        self,
        lat,
        lon,
        start_date: dt | None = None,
        end_date: dt | None = None,
        metric=False,
    ):
        return self._daily_forecast_from_location_info(
            location_info=[lat, lon],
            start_date=start_date,
            end_date=end_date,
            metric=metric,
        )

    def _daily_forecast_from_location_info(
        self,
        location_info,
        start_date: dt | None = None,
        end_date: dt | None = None,
        metric=False,
    ):
        if not start_date:
            start_date = dt.today()

        lat, lon = location_info
        params = {
            "whichClient": "NDFDgen",
            "lat": lat,
            "lon": lon,
            "product": "time-series",
            # NDFD ignores dates that carry fractional seconds.
            "begin": start_date.isoformat(timespec="seconds"),
            "end": None if end_date is None else end_date.isoformat(timespec="seconds"),
            "Unit": "m" if metric else "e",
            "wspd": "wspd",
            "wdir": "wdir",
            "waveh": "waveh",
            "wgust": "wgust",
            "Submit": "Submit",
        }
        response = self.make_request(API_PATH[Endpoints.FORECASTS.value], params=params)
        xml_root = ET.fromstring(response.encode("utf-8"))
        if xml_root.tag == "error":
            # NOAA reports a rejected request in the body, with status 200.
            reason = xml_root.findtext("pre", default="no reason given")
            raise NOAAException(f"NOAA rejected the forecast request: {reason}")
        parsed = self.xslt_transform(xml_root)

        return loads(str(parsed))

    def __group_parameters_by_time(self, parameters: dict):
        """Group DWML as XSLT by observation recorded.

        Args:
            parameters (dict): XSLT object

        Returns:
            (
                str,
                defaultdict(
                    ForecastKey,
                    {
                        "value": int,
                        "label": str,
                        "units": str,
                    }
                )
            )

        """
        # TODO: refactor
        # XSLT flatten data instead?
        ele_map = {
            "direction": ("wind-direction",),
            "wind": (
                "gust",
                "sustained",
            ),
            "water-state": ("significant",),
        }
        default_val = {"value": NO_NUMERIC_VALUE}
        groupedby_timestamp: dict[str, dict] = defaultdict(
            lambda: defaultdict(
                dict,
                wave_height=default_val,
                wind_direction=default_val,
                wind_speed_gust=default_val,
                wind_speed=default_val,
            )
        )
        for k, v in parameters.items():
            for key in v:
                if key in ele_map[k]:
                    for period in parameters[k][key]["periods"]:
                        timestamp = period["start-time"]
                        new_key = "_".join(
                            parameters[k][key]["name"].lower().split(" ")
                        )
                        groupedby_timestamp[timestamp][new_key] = {
                            "value": period["value"],
                            # TODO: transform to proper label here
                            "label": parameters[k][key]["name"],
                            "units": parameters[k][key]["units"],
                        }

        return groupedby_timestamp


def _without_offset(moment: dt, padding: timedelta) -> dt:
    if moment.tzinfo is None:
        return moment
    return moment.astimezone(UTC).replace(tzinfo=None) + padding
