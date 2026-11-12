"""Errors raised by pybuoy."""

from collections.abc import Callable
from functools import wraps
from xml.etree.ElementTree import ParseError as XmlParseError


class PybuoyError(Exception):
    """Base class for every error pybuoy raises."""


class ParseError(PybuoyError):
    """A response was not in the format pybuoy expects."""


class RequestError(PybuoyError):
    """NOAA or NDBC could not be reached, or gave an answer pybuoy refuses.

    That is an error status, a forecast request NOAA rejects, or a body larger
    than 16 MB.
    """

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status
        """HTTP status of the answer, or ``None`` if no complete answer arrived."""


class StationNotFoundError(PybuoyError):
    """NDBC has no such station, or the station does not publish the dataset."""


def _parser[**P, T](parse: Callable[P, T]) -> Callable[P, T]:
    """Make a parsing function raise ``ParseError`` for malformed input."""

    @wraps(parse)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return parse(*args, **kwargs)
        except (KeyError, ValueError, OverflowError, XmlParseError) as error:
            raise ParseError(f"Unexpected response format: {error!r}") from error

    return wrapper
