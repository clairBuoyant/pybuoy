"""pybuoy exception classes."""

from requests import HTTPError  # type: ignore


class BaseException(Exception):
    """Base Exception that all other exception classes extend."""

    ...


class HTTPException(HTTPError): ...


class NDBCException(BaseException): ...


class NOAAException(BaseException): ...


class DWMLException(NOAAException):
    """NOAA DWML Exception.

    ref: https://graphical.weather.gov/xml/DWMLgen/schema/DWML.xsd
    """

    ...
