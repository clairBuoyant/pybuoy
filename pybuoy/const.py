"""pybuoy constants."""

from enum import Enum
from typing import Literal

from pybuoy.endpoints import API_PATH as API_PATH


class Endpoints(Enum):
    ACTIVE_STATIONS = "active_stations"
    FORECASTS = "forecasts"
    REALTIME = "realtime2"


class RealtimeDatasets(Enum):
    spec = "spec"
    txt = "txt"


RealtimeDatasetsValues = Literal["spec", "txt"]

__version__ = "0.5.10"
