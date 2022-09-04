"""Provide the ParserMixin class."""
from datetime import datetime as dt
from typing import Literal, Type, TypeVar, Union, overload
from xml.etree.cElementTree import Element, fromstring

from pybuoy.const import RealtimeDatasets, RealtimeDatasetsValues
from pybuoy.observation import MeteorologicalObservation, WaveSummaryObservation
from pybuoy.observation.observations import (
    MeteorologicalObservations,
    WaveSummaryObservations,
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


T = TypeVar("T")


class ParserMixin:
    """Interface for Buoy classes and its composites."""

    @overload
    def parse(
        self,
        data: str,
        dataset: Literal["txt"],
        __observation_type: Type[MeteorologicalObservations],
    ) -> MeteorologicalObservations:
        ...

    @overload
    def parse(
        self,
        data: str,
        dataset: Literal["spec"],
        __observation_type: Type[WaveSummaryObservations],
    ) -> WaveSummaryObservations:
        ...

    @overload
    def parse(
        self, data: str, dataset: RealtimeDatasetsValues, __observation_type: Type[str]
    ) -> str:
        ...

    # TODO: rework signature
    def parse(
        self,
        data: str,
        dataset: RealtimeDatasetsValues,
        __observation_type: Type[T],
    ):
        observations_class_instance = __observation_type()
        if isinstance(observations_class_instance, MeteorologicalObservations):
            return self.__clean_realtime_data(
                data, RealtimeDatasets.txt.value, observations_class_instance
            )
        if isinstance(observations_class_instance, WaveSummaryObservations):
            return self.__clean_realtime_data(
                data, RealtimeDatasets.spec.value, observations_class_instance
            )
        return data

    def _clean_activestation_data(self, data: str):
        xml_tree = fromstring(data)
        return [XmlToDict(el) for el in xml_tree.findall("station")]

    @overload
    def __clean_realtime_data(
        self, data: str, dataset: Literal["txt"], t: MeteorologicalObservations
    ) -> MeteorologicalObservations:
        ...

    @overload
    def __clean_realtime_data(
        self, data: str, dataset: Literal["spec"], t: WaveSummaryObservations
    ) -> WaveSummaryObservations:
        ...

    def __clean_realtime_data(
        self, data: str, dataset: Union[Literal["txt"], Literal["spec"]], t: T
    ):
        # TODO: Error handling when request not successful
        if data is None:
            return None
        rows = data.strip().split("\n")

        headers = [" ".join(row.split()).split(" ") for row in rows[0:2]]
        header_offset = 5  # end of datetime columns
        headers_without_dates = headers[0][header_offset:]

        # TODO: consider csv module
        realtime_data = t
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
            if dataset == RealtimeDatasets.txt.value:
                values = {
                    MeteorologicalKey[headers_without_dates[idx]]: value
                    for idx, value in enumerate(record_array[header_offset:])
                }
                observation = MeteorologicalObservation(
                    values,
                    date_recorded,
                )
            elif dataset == RealtimeDatasets.spec.value:
                values = {
                    WaveSummaryKey[headers_without_dates[idx]]: value
                    for idx, value in enumerate(record_array[header_offset:])
                }
                observation = WaveSummaryObservation(
                    values,
                    date_recorded,
                )
            # TODO: refactor to use setter method and fix type
            realtime_data.reports.append(  # type: ignore
                observation
            ) if observation is not None else None
        return realtime_data
