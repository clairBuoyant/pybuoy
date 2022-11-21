from pybuoy.api.base import ApiBase
from pybuoy.const import API_PATH, Endpoints
from datetime import datetime as dt
import xml.etree.ElementTree as ET

class Forecasts(ApiBase):
    def get(self, lat: int, lon: int, beginDate: str, endDate: str):
        # TODO: (LOW) add error checking for dates so they are passed in as strings in ISO format
        # If not in ISO format throw user friendly exception
        # TODO: (LOW) investigate if there's a better way of passing params dict
        response = self.make_request(API_PATH[Endpoints.FORECASTS.value], params={
            "whichClient":"NDFDgen",
            "lat": lat,
            "lon": lon,
            "product": "time-series",
            "begin": dt.fromisoformat(beginDate).isoformat(),
            "end": dt.fromisoformat(endDate).isoformat(),
            "Unit": "e",
            "wspd": "wspd",
            "wdir": "wdir",
            "waveh": "waveh",
            "wgust": "wgust",
            "Submit": "Submit"
        })
        data = self.etree_to_dict(ET.fromstring(response))['dwml']['data']
        forecast_data = []
        time_stamps = data['time-layout']['start-valid-time']
        parameters = data['parameters']
        for i, time_stamp in enumerate(time_stamps):
            forecast_data.append({
                "datetime": time_stamp,
                "wind_direction": parameters['direction']['value'][i],
                "wind_speed": parameters['wind-speed'][0]['value'][i],
                "wind_gust": parameters['wind-speed'][1]['value'][i],
                "wave_height": parameters['water-state']['waves']['value'][i]
            })
        return forecast_data