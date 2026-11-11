"""Provide the ParserMixin class."""

from os.path import dirname, join
from xml.etree.ElementTree import fromstring

import lxml.etree as ET  # type: ignore


class ParserMixin:
    """Parser mixin supports handling of third-party data."""

    def __init__(self) -> None:
        self.__set_xslt_transform()

    @property
    def xslt_transform(self) -> ET.XSLT:
        return self._xslt_transform

    def _clean_activestation_data(self, data: str):
        xml_tree_root = fromstring(data.encode("utf-8"))
        return [dict(el.items()) for el in xml_tree_root.findall("station")]

    def __set_xslt_transform(self, xsl_filename="noaa.xsl"):
        forecast_xslt = ET.parse(join(dirname(__file__), xsl_filename))
        self._xslt_transform = ET.XSLT(forecast_xslt)
