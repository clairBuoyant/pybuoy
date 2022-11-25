from pybuoy.api.base import ApiBase
from pybuoy.const import API_PATH, Endpoints
from datetime import datetime as dt
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

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
                mapping[time_layout]["wind_speed_sustained"] = wind_speed_sustained_values
            if layout_key == wind_speed_gust.attrib['time-layout']:
                mapping[time_layout]["wind_speed_gust"] = wind_speed_gust_values
            if layout_key == wind_direction.attrib['time-layout']:
                mapping[time_layout]["wind_direction"] = wind_direction_values
            if layout_key == water_state.attrib['time-layout']:
                mapping[time_layout]["wave"] = wave_values
            element_mappings.append(mapping)

        # mapping the data with actual time_stamps
        timed_mappings = []
        for element_mapping in element_mappings:
            time_layout = next(iter(element_mapping))
            time_stamps = self.__get_values(time_layout, "start-valid-time")
            mapping_holder = []
            for i, time_stamp in enumerate(time_stamps):
                timed_mapping = {time_stamp : {}}
                timed_mapping[time_stamp]["wind_speed_sustained"] = element_mapping[time_layout]["wind_speed_sustained"][i] if "wind_speed_sustained" in element_mapping[time_layout] else None
                timed_mapping[time_stamp]["wind_speed_gust"] = element_mapping[time_layout]["wind_speed_gust"][i] if "wind_speed_gust" in element_mapping[time_layout] else None
                timed_mapping[time_stamp]["wind_direction"] = element_mapping[time_layout]["wind_direction"][i] if "wind_direction" in element_mapping[time_layout] else None                    
                timed_mapping[time_stamp]["wave"] = element_mapping[time_layout]["wave"][i] if "wave" in element_mapping[time_layout] else None
                mapping_holder.append(timed_mapping)
            timed_mappings.append(mapping_holder)
        
        # Syncing the data to make one big final synced mapping
        head_timed_mapping = self.__get_longest_list(timed_mappings)
        

        return timed_mappings

    def __get_values(self, element: Element, value: str) -> list[str]:
        element_text_list = []
        element_list = element.findall(value)
        for element in element_list:
            element_text_list.append(element.text)
        return element_text_list

    def __get_longest_list(self, array: list):
        index = 0
        max_len = 0
        for i, arr in enumerate(array):
            if len(arr) > max_len:
                index = i 
                max_len = len(arr)
        return array.pop(index)