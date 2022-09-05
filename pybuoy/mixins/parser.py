"""Provide the ParserMixin class."""
from datetime import datetime as dt
from xml.etree.cElementTree import Element, fromstring

from pybuoy.const import RealtimeDatasets, RealtimeDatasetsValues
from pybuoy.exceptions import BuoyException
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


# TODO: refactor and incorporate mixin
class ParserMixin:
    """Interface for Buoy classes and its composites."""

    def parse(
        self,
        data: str,
        dataset: RealtimeDatasetsValues,
    ) -> MeteorologicalObservations | WaveSummaryObservations | str:
        obs = self.__clean_realtime_data(data=data, dataset=dataset)
        # TODO: refine error handling
        if obs is None or len(obs) == 0:
            raise BuoyException

        match dataset:
            case RealtimeDatasets.spec.value:
                # ? overloading can be an alternative
                wave_obs: list[WaveSummaryObservation] = obs  # type: ignore
                return WaveSummaryObservations(observations=wave_obs)
            case RealtimeDatasets.txt.value:
                met_obs: list[MeteorologicalObservation] = obs  # type: ignore
                return MeteorologicalObservations(observations=met_obs)
            case _:
                return data

    def _clean_activestation_data(self, data: str):
        xml_tree = fromstring(data)
        return [XmlToDict(el) for el in xml_tree.findall("station")]

    def __clean_realtime_data(
        self, data: str, dataset: RealtimeDatasetsValues
    ) -> list[MeteorologicalObservation] | list[WaveSummaryObservation]:
        if data is None:
            # TODO: handle when request not successful
            raise BuoyException

        # TODO: consider csv module
        rows = data.strip().split("\n")
        headers = [" ".join(row.split()).split(" ") for row in rows[0:2]]
        header_offset = 5  # end of datetime columns
        headers_without_dates = headers[0][header_offset:]

        obs = []
        for row in rows[2:]:
            record_array = " ".join(row.split()).split(" ")
            date_recorded = dt(
                int(record_array[0]),
                int(record_array[1]),
                int(record_array[2]),
                int(record_array[3]),
                int(record_array[4]),
            )
            if dataset == RealtimeDatasets.txt.value:
                observation = self.__parse_meteorological_record(
                    date_recorded=date_recorded,
                    headers=headers_without_dates,
                    records=record_array[header_offset:],
                )
            elif dataset == RealtimeDatasets.spec.value:
                observation = self.__parse_wave_summary_record(
                    date_recorded=date_recorded,
                    headers=headers_without_dates,
                    records=record_array[header_offset:],
                )
            obs.append(observation) if observation is not None else None

        return obs

    # TODO: refactor
    def __parse_meteorological_record(self, date_recorded: dt, headers, records):
        values: dict[MeteorologicalKey, str] = {
            MeteorologicalKey[headers[idx]]: value for idx, value in enumerate(records)
        }
        return MeteorologicalObservation(values, date_recorded)

    # TODO: combine with above
    def __parse_wave_summary_record(self, date_recorded: dt, headers, records):
        values: dict[WaveSummaryKey, str] = {
            WaveSummaryKey[headers[idx]]: value for idx, value in enumerate(records)
        }
        return WaveSummaryObservation(values, date_recorded)
