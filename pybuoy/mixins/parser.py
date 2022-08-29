"""Provide the ParserMixin class."""
from datetime import datetime as dt
from xml.etree.cElementTree import Element, fromstring

from pybuoy.const import RealtimeDatasets
from pybuoy.observation import (
    MeteorologicalObservation,
    Observations,
    WaveSummaryObservation,
)
from pybuoy.unit_mappings import MeteorologicalKey, WaveSummaryKey


class XmlToDict(dict):
    def __init__(self, data: Element):
        if data.items():
            self.update(dict(data.items()))
        for element in data:
            if element:
                # treat like dict - assumes that if the first two tags
                # in a series are different, then all are different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    tmp_dict: dict[str, XmlToDict] | XmlToDict = XmlToDict(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    tmp_dict = {element[0].tag: XmlToDict(element)}
                # if the tag has attributes, add those to the dict
                if isinstance(element, XmlToDict) and element.items():
                    tmp_dict.update(dict(element.items()))
                self.update({element.tag: tmp_dict})
            # assumes an attribute in a tag without any text.
            elif element.items():
                self.update({element.tag: dict(element.items())})
            else:
                self.update({element.tag: element.text})


class ParserMixin:
    """Interface for Buoy classes and its composites."""

    def parse(self, data: str, dataset: str = RealtimeDatasets.TXT.value):
        return (
            data
            if dataset != RealtimeDatasets.TXT.value
            and dataset != RealtimeDatasets.SPEC.value
            else self.__clean_realtime_data(data=data, dataset=dataset)
        )

    def _clean_activestation_data(self, data: str):
        xml_tree = fromstring(data)
        return [XmlToDict(el) for el in xml_tree.findall("station")]

    def __clean_realtime_data(self, data: str, dataset: str) -> Observations:
        # TODO: Error handling when request not successful
        if data is None:
            return None
        rows = data.strip().split("\n")

        headers = [" ".join(row.split()).split(" ") for row in rows[0:2]]
        header_offset = 5  # end of datetime columns
        headers_without_dates = headers[0][header_offset:]

        # TODO: consider csv module
        realtime_data = Observations()
        for row in rows[2:]:
            record_array = " ".join(row.split()).split(" ")
            date_recorded = dt(
                int(record_array[0]),
                int(record_array[1]),
                int(record_array[2]),
                int(record_array[3]),
                int(record_array[4]),
            )

            observation: MeteorologicalObservation | WaveSummaryObservation
            values: dict[MeteorologicalKey, str] | dict[WaveSummaryKey, str]
            if dataset == RealtimeDatasets.TXT.value:
                values = {
                    MeteorologicalKey[headers_without_dates[idx]]: value
                    for idx, value in enumerate(record_array[header_offset:])
                }
                observation = MeteorologicalObservation(
                    values,
                    date_recorded,
                )
            elif dataset == RealtimeDatasets.SPEC.value:
                values = {
                    WaveSummaryKey[headers_without_dates[idx]]: value
                    for idx, value in enumerate(record_array[header_offset:])
                }
                observation = WaveSummaryObservation(
                    values,
                    date_recorded,
                )
            # TODO: refactor to use setter method
            realtime_data.reports.append(
                observation
            ) if observation is not None else None
        return realtime_data
