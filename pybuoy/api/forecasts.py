from datetime import datetime as dt
from json import loads
from os.path import dirname, join
from typing import Optional

import lxml.etree as ET

from pybuoy.api.base import ApiBase
from pybuoy.const import API_PATH, Endpoints

# from pybuoy.observation.observation import MeteorologicalPrediction
# from pybuoy.observation.observations import MeteorologicalPredictions
# from pybuoy.unit_mappings import MeteorologicalKey


class Forecasts(ApiBase):
    # https://graphical.weather.gov/xml/rest.php
    def get(self, lat: float, lon: float, beginDate: str, endDate: str):
        dwml_data = self.forecast_by_lat_lon(
            lat=lat,
            lon=lon,
            start_date=dt.fromisoformat(beginDate),
            end_date=dt.fromisoformat(endDate),
        )
        # TODO: serialize into python objects for end-users
        # MeteorologicalPredictions(observations=dwml_data)
        return dwml_data

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
