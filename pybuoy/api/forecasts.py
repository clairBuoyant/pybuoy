from collections import defaultdict
from datetime import datetime as dt
from json import loads
from os.path import dirname, join
from typing import Optional

import lxml.etree as ET

from pybuoy.api.base import ApiBase
from pybuoy.const import API_PATH, Endpoints
from pybuoy.observation import ForecastObservation, ForecastObservations


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
        # TODO: serialize into python objects for end-users
        predictions = [
            ForecastObservation(grouped[key], dt.fromisoformat(key))
            for key in grouped.keys()
        ]
        parsed = ForecastObservations(observations=predictions, repr_limit=10)
        return parsed

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

        # TODO: test array of tuples
        # https://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?lat=40.369&lon=-73.702&product=time-series&begin=2023-01-01T00:00:00&end=2023-02-20T00:00:00&waveh=waveh&wspd=wspd&wgust=wgust&wdir=wdir
        # ? does order of query-string parameter matter
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

        """Task List
        # TODO: XSL Parsing
        #  * load XSL file via _init_
        #  * set transform as class method on instantiation
        """
        directory = dirname(__file__)
        xsl_file = join(directory, "noaa.xsl")
        xslt = ET.parse(xsl_file)
        transform = ET.XSLT(xslt)
        dom = ET.fromstring(response)
        x = transform(dom)
        # /end (Task List)

        json_load = loads(str(x))
        return json_load

    # TODO: should XSLT flatten data instead
    # TODO: add documentation, if this will be merged
    def __group_parameters_by_time(self, parameters: dict):
        # TODO: refactor mapping
        ele_map = {
            "direction": ("wind-direction",),
            "wind": (
                "gust",
                "sustained",
            ),
            "water-state": ("significant",),
        }
        default_val = {"value": "nan"}
        # TODO: initialize defaults dynamically on _init_
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
                        # TODO: eval ForecastObservation
                        groupedby_timestamp[timestamp][new_key] = {
                            "value": period["value"],
                            # TODO: transform to proper label here
                            "label": parameters[k][key]["name"],
                            "_units": parameters[k][key]["units"],
                            "_k": k,
                        }
        # TODO: document structure
        return groupedby_timestamp
