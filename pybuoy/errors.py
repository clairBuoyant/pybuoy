"""Errors raised by pybuoy."""

from collections.abc import Callable
from functools import wraps
from xml.etree.ElementTree import ParseError as XmlParseError


class PybuoyError(Exception):
    """Base class for every error pybuoy raises."""


class RequestError(PybuoyError):
    """NOAA or NDBC could not be reached, or answered with an error status."""

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status
        """HTTP status of the answer, or ``None`` if there was no answer."""


class StationNotFoundError(PybuoyError):
    """NDBC has no such station, or the station does not publish the dataset."""


class ParseError(PybuoyError):
    """A response was not in the format pybuoy expects."""


def parser[**P, T](parse: Callable[P, T]) -> Callable[P, T]:
    """Make a parsing function raise ``ParseError`` for malformed input."""

    @wraps(parse)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return parse(*args, **kwargs)
        except (KeyError, ValueError, XmlParseError) as error:
            raise ParseError(f"Unexpected response format: {error!r}") from error

    return wrapper
