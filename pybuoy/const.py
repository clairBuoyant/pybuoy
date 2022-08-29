"""pybuoy constants."""
from enum import Enum

from pybuoy.endpoints import API_PATH as API_PATH  # noqa: F401


class Endpoints(Enum):
    ACTIVE_STATIONS = "active_stations"
    REALTIME = "realtime2"


class RealtimeDatasets(Enum):
    SPEC = "spec"
    TXT = "txt"


NO_VALUE = "MM"

__version__ = "0.4.0"
