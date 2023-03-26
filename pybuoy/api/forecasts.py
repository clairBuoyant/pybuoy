from collections import defaultdict
from datetime import datetime as dt
from json import loads
from typing import Optional

import lxml.etree as ET  # type: ignore

from pybuoy.api.base import ApiBase
from pybuoy.const import API_PATH, Endpoints
from pybuoy.observation import ForecastObservation, ForecastObservations
from pybuoy.unit_mappings import NO_NUMERIC_VALUE


class Forecasts(ApiBase):
    # https://graphical.weather.gov/xml/rest.php
    def get(self, lat: float, lon: float, start_date: str, end_date: str):
        dwml_data = self.forecast_by_lat_lon(
            lat=lat,
            lon=lon,
            start_date=dt.fromisoformat(start_date),
            end_date=dt.fromisoformat(end_date),
        )
        grouped = self.__group_parameters_by_time(dwml_data["data"]["parameters"])

        return ForecastObservations(
            observations=[
                ForecastObservation(grouped[key], dt.fromisoformat(key))
                for key in grouped.keys()
            ],
            repr_limit=10,
        )

    def forecast_by_lat_lon(
        self,
        lat,
        lon,
        start_date: Optional[dt] = None,
        end_date: Optional[dt] = None,
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
        start_date: Optional[dt] = None,
        end_date: Optional[dt] = None,
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
            "begin": start_date.isoformat(),
            "end": None if end_date is None else end_date.isoformat(),
            "Unit": "m" if metric else "e",
            "wspd": "wspd",
            "wdir": "wdir",
            "waveh": "waveh",
            "wgust": "wgust",
            "Submit": "Submit",
        }
        response = self.make_request(API_PATH[Endpoints.FORECASTS.value], params=params)
        xml_root = ET.fromstring(response)
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
            for key in v.keys():
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
