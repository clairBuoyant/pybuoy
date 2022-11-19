from pybuoy.api.base import ApiBase
from pybuoy.const import API_PATH, Endpoints
from datetime import datetime as dt
import xml.etree.ElementTree as ET

class Forecasts(ApiBase):
    # TODO: (HIGH) implement get method with XML parsing
    def get(self, lat: int, lon: int, beginDate: dt, endDate: dt):
        # All this does rn is make a request and returns an XML text, there is no parsing
        response = self.make_request(API_PATH[Endpoints.FORECASTS.value], params={
            "whichClient":"NDFgen",
            "lat": lat,
            "lon": lon,
            "product": "time-series",
            "begin": beginDate,
            "end": endDate,
            "Unit": "e",
            "wspd": "wspd",
            "wdir": "wdir",
            "waveh": "waveh",
            "wgust": "wgust",
            "Submit": "Submit"
        })
        root = ET.fromstring(response)
        print(root)
        return root