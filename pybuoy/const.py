"""pybuoy constants."""

from enum import Enum
from typing import Literal

from pybuoy.endpoints import API_PATH as API_PATH  # noqa: F401


class Endpoints(Enum):
    ACTIVE_STATIONS = "active_stations"
    FORECASTS = "forecasts"
    REALTIME = "realtime2"


class RealtimeDatasets(Enum):
    data_spec = "data_spec"
    ocean = "ocean"
    spec = "spec"
    supl = "supl"
    swdir = "swdir"
    swdir2 = "swdir2"
    swr1 = "swr1"
    swr2 = "swr2"
    txt = "txt"


RealtimeDatasetsValues = Literal[
    "data_spec",
    "ocean",
    "spec",
    "supl",
    "swdir",
    "swdir2",
    "swr1",
    "swr2",
    "txt",
]

__version__ = "0.5.5"
