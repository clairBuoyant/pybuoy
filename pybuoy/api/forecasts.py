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
        # Code that I paste into terminal
        # Will delete when finished with forecast development
        # import pybuoy
        # buoy = pybuoy.Buoy()
        # buoy.forecasts.get(40.369, -73.702531, 2022-11-19, 2022-11-22)
        root = ET.fromstring(response)
        for time in root.iter("start-valid-time"):
            print(time.text)
        for wind_speed in root.findall(".//*[@type='sustained']/value"):
            print(wind_speed.text)
        for wind_direction in root.findall(".//direction/value"):
            print(wind_direction.text)
        for wind_gust in root.findall(".//*[@type='gust']/value"):
            print(wind_gust.text)
        for wave in root.findall(".//waves/value"):
            print(wave.text)
        return "End of method"