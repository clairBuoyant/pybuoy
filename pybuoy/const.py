"""pybuoy constants."""
from enum import Enum
from typing import Literal, Union

from pybuoy.endpoints import API_PATH as API_PATH  # noqa: F401


class Endpoints(Enum):
    ACTIVE_STATIONS = "active_stations"
    REALTIME = "realtime2"


class RealtimeDatasets(Enum):
    spec = "spec"
    txt = "txt"


RealtimeDatasetsValues = Union[RealtimeDatasets, Literal["spec", "txt"]]

NO_VALUE = "MM"

__version__ = "0.4.0"
