"""Provide the ParserMixin class."""

from os.path import dirname, join

import lxml.etree as ET  # type: ignore


class ParserMixin:
    """Parser mixin supports handling of third-party data."""

    def __init__(self) -> None:
        self.__set_xslt_transform()

    @property
    def xslt_transform(self) -> ET.XSLT:
        return self._xslt_transform

    def __set_xslt_transform(self, xsl_filename="noaa.xsl"):
        forecast_xslt = ET.parse(join(dirname(__file__), xsl_filename))
        self._xslt_transform = ET.XSLT(forecast_xslt)
