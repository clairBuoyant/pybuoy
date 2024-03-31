"""Provide the ParserMixin class."""

from collections import defaultdict
from datetime import datetime as dt
from os.path import dirname, join
from typing import Any
from xml.etree.ElementTree import Element, fromstring

import lxml.etree as ET  # type: ignore

from pybuoy.const import RealtimeDatasets, RealtimeDatasetsValues
from pybuoy.exceptions import NDBCException
from pybuoy.observation import MeteorologicalObservation, WaveSummaryObservation
from pybuoy.observation.observations import (
    MeteorologicalObservations,
    WaveSummaryObservations,
)
from pybuoy.unit_mappings import MeteorologicalKey, WaveSummaryKey


class ParserMixin:
    """Parser mixin supports handling of third-party data."""

    def __init__(self) -> None:
        self.__set_xslt_transform()

    def etree_to_dict(self, element: Element):
        """Parse XML Element to dictionary."""
        from_etree: dict[str, dict[str, Any] | Any] = {
            element.tag: {} if element.attrib else None
        }
        children = list(element)
        if children:
            parsed_children = defaultdict(list)
            for child in map(self.etree_to_dict, children):
                for key, value in child.items():
                    parsed_children[key].append(value)
            from_etree = {
                element.tag: {
                    key: value[0] if len(value) == 1 else value
                    for key, value in parsed_children.items()
                }
            }
        if element.attrib:
            from_etree[element.tag].update(
                (key, value) for key, value in element.attrib.items()
            )
        if element.text:
            text = element.text.strip()
            if children or element.attrib:
                if text:
                    from_etree[element.tag]["text"] = text
            else:
                from_etree[element.tag] = text
        return from_etree

    def parse(
        self,
        data: str,
        dataset: RealtimeDatasetsValues,
    ) -> MeteorologicalObservations | WaveSummaryObservations | str:
        obs = self.__clean_realtime_data(data=data, dataset=dataset)
        # TODO: refine error handling
        if obs is None or len(obs) == 0:
            raise NDBCException

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

    @property
    def xslt_transform(self) -> ET.XSLT:
        return self._xslt_transform

    # TODO: consider station class/dto like observations
    def _clean_activestation_data(self, data: str):
        xml_tree_root = fromstring(data)
        # TODO: consider incorporating `etree_to_dict`
        return [dict(el.items()) for el in xml_tree_root.findall("station")]

    # TODO: fix missing latest row
    def __clean_realtime_data(
        self, data: str, dataset: RealtimeDatasetsValues
    ) -> list[MeteorologicalObservation] | list[WaveSummaryObservation]:
        if data is None:
            # TODO: handle when request not successful
            raise NDBCException

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
            # TODO: investigate adding Strategy Pattern here
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

    def __parse_meteorological_record(self, date_recorded: dt, headers, records):
        values: dict[MeteorologicalKey, str] = {
            MeteorologicalKey[headers[idx]]: value for idx, value in enumerate(records)
        }
        return MeteorologicalObservation(values, date_recorded)

    # TODO: refactor (e.g., combine with __parse_meteorological_record)
    def __parse_wave_summary_record(self, date_recorded: dt, headers, records):
        values: dict[WaveSummaryKey, str] = {
            WaveSummaryKey[headers[idx]]: value for idx, value in enumerate(records)
        }
        return WaveSummaryObservation(values, date_recorded)

    def __set_xslt_transform(self, xsl_filename="noaa.xsl"):
        forecast_xslt = ET.parse(join(dirname(__file__), xsl_filename))
        self._xslt_transform = ET.XSLT(forecast_xslt)
