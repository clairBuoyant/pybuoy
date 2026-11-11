"""pybuoy constants."""

from enum import Enum

from pybuoy.endpoints import API_PATH as API_PATH


class Endpoints(Enum):
    FORECASTS = "forecasts"


__version__ = "0.5.11"
