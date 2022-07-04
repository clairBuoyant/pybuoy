"""Provide the ParserMixin class."""
from datetime import datetime as dt
from xml.etree import cElementTree as et

from pybuoy.observation import Observation
from pybuoy.unit_mappings import METEOROLOGICAL


class XmlToDict(dict):
    def __init__(self, data):
        if data.items():
            self.update(dict(data.items()))
        for element in data:
            if element:
                # treat like dict - assumes that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    tmp_dict = XmlToDict(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    tmp_dict = {element[0].tag: XmlToDict(element)}  # TODO: fix inconsistency
                # if the tag has attributes, add those to the dict
                if element.items():
                    tmp_dict.update(dict(element.items()))
                self.update({element.tag: tmp_dict})
            # this assumes that if you've got an attribute in a tag without
            # any text.
            elif element.items():
                self.update({element.tag: dict(element.items())})
            else:
                self.update({element.tag: element.text})


class ParserMixin:
    """Interface for Buoy classes and its composites."""

    def parse(self, data: str, dataset: str = "txt"):
        return data if dataset != "txt" else self.__clean_realtime_data(data=data)

    def _clean_activestation_data(self, data: str):

        xml_tree = et.fromstring(data)
        return [XmlToDict(el) for el in xml_tree.findall("station")]

    def __clean_realtime_data(self, data: str):
        rows = data.strip().split("\n")
        headers = [" ".join(row.split()).split(" ") for row in rows[0:2]]
        realtime_data = []
        for row in rows[2:]:
            record_array = " ".join(row.split()).split(" ")
            date_recorded = dt(
                int(record_array[0]),
                int(record_array[1]),
                int(record_array[2]),
                int(record_array[3]),
                int(record_array[4]),
            )
            observations_for_record = []
            header_offset = 5
            for idx, value in enumerate(record_array[header_offset:]):
                observations_for_record.append(
                    Observation(
                        value, METEOROLOGICAL[headers[0][idx + header_offset]], date_recorded
                    )
                )
            realtime_data.append(observations_for_record)
        return realtime_data
