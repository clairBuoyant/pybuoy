from pybuoy.api.base import ApiBase
from pybuoy.const import API_PATH, Endpoints
from datetime import datetime as dt
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from pybuoy.unit_mappings import MeteorologicalKey
from pybuoy.observation.observation import MeteorologicalPrediction
from pybuoy.observation.observations import MeteorologicalPredictions

class Forecasts(ApiBase):
    # https://graphical.weather.gov/xml/mdl/XML/Design/MDL_XML_Design.pdf
    def get(self, lat: int, lon: int, beginDate: str, endDate: str):
        # TODO: (LOW) add error checking for dates so they are passed in as strings in ISO format
        # If not in ISO format throw user friendly exception
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

        # TODO: (MEDIUM) Refactor code into parserMixin?
        element_mappings = []
        data = ET.fromstring(response)
        time_layouts = data.findall(".//time-layout")
        wind_speed_sustained = data.find(".//*[@type='sustained']")
        wind_speed_sustained_values = self.__get_values(wind_speed_sustained, "value")
        wind_speed_gust = data.find(".//*[@type='gust']")
        wind_speed_gust_values = self.__get_values(wind_speed_gust, "value")
        wind_direction = data.find(".//direction")
        wind_direction_values = self.__get_values(wind_direction, "value")
        water_state = data.find('.//water-state')
        wave_values = self.__get_values(water_state.find('waves'), "value")

        # mapping data to time stamp elements
        for time_layout in time_layouts:
            layout_key = time_layout.find("layout-key").text
            mapping = { time_layout : {} }
            if layout_key == wind_speed_sustained.attrib['time-layout']:
                mapping[time_layout][MeteorologicalKey.WSPD] = wind_speed_sustained_values
            if layout_key == wind_speed_gust.attrib['time-layout']:
                mapping[time_layout][MeteorologicalKey.GST] = wind_speed_gust_values
            if layout_key == wind_direction.attrib['time-layout']:
                mapping[time_layout][MeteorologicalKey.WDIR] = wind_direction_values
            if layout_key == water_state.attrib['time-layout']:
                mapping[time_layout][MeteorologicalKey.WVHT] = wave_values
            element_mappings.append(mapping)

        # mapping the data with actual time-stamp values: start-valid-time
        timed_mappings = []
        for element_mapping in element_mappings:
            time_layout = next(iter(element_mapping))
            time_stamps = self.__get_values(time_layout, "start-valid-time")
            mapping_holder = {}
            for i, time_stamp in enumerate(time_stamps):
                forecast_values = {
                    MeteorologicalKey.WSPD: "nan",
                    MeteorologicalKey.GST: "nan",
                    MeteorologicalKey.WDIR: "nan",
                    MeteorologicalKey.WVHT: "nan"
                }

                if MeteorologicalKey.WSPD in element_mapping[time_layout]:
                    forecast_values[MeteorologicalKey.WSPD] = element_mapping[time_layout][MeteorologicalKey.WSPD][i]
                if MeteorologicalKey.GST in element_mapping[time_layout]:
                    forecast_values[MeteorologicalKey.GST] = element_mapping[time_layout][MeteorologicalKey.GST][i]
                if MeteorologicalKey.WDIR in element_mapping[time_layout]:
                    forecast_values[MeteorologicalKey.WDIR] = element_mapping[time_layout][MeteorologicalKey.WDIR][i]
                if MeteorologicalKey.WVHT in element_mapping[time_layout]:
                    forecast_values[MeteorologicalKey.WVHT] = element_mapping[time_layout][MeteorologicalKey.WVHT][i]

                mapping_holder[time_stamp] = forecast_values
            timed_mappings.append(mapping_holder)
        
        synced_timed_mapping = self.__get_longest_mapping(timed_mappings)
        for timed_mapping in timed_mappings:
            for key in timed_mapping.keys():
                if timed_mapping[key][MeteorologicalKey.WSPD] != "nan":
                    synced_timed_mapping[key][MeteorologicalKey.WSPD] = timed_mapping[key][MeteorologicalKey.WSPD]
                if timed_mapping[key][MeteorologicalKey.GST] != "nan":
                    synced_timed_mapping[key][MeteorologicalKey.GST] = timed_mapping[key][MeteorologicalKey.GST]
                if timed_mapping[key][MeteorologicalKey.WDIR] != "nan":
                    synced_timed_mapping[key][MeteorologicalKey.WDIR] = timed_mapping[key][MeteorologicalKey.WDIR]
                if timed_mapping[key][MeteorologicalKey.WVHT] != "nan":
                    synced_timed_mapping[key][MeteorologicalKey.WVHT] = timed_mapping[key][MeteorologicalKey.WVHT]
        
        predictions = [MeteorologicalPrediction(synced_timed_mapping[key], dt.fromisoformat(key)) for key in synced_timed_mapping.keys()]

        return MeteorologicalPredictions(observations=predictions)

    def __get_values(self, element: Element, value: str) -> list[str]:
        element_text_list = []
        element_list = element.findall(value)
        for element in element_list:
            element_text_list.append(element.text)
        return element_text_list

    def __get_longest_mapping(self, array: list) -> dict:
        index = 0
        max_len = 0
        for i, mapping in enumerate(array):
            if len(mapping.keys()) > max_len:
                index = i 
                max_len = len(mapping.keys())
        return array.pop(index)