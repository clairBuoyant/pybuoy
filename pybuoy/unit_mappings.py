"""Mapping key to unit for forecasts."""

from enum import Enum
from typing import TypedDict

NO_NUMERIC_VALUE = "MM"


class ForecastKey(Enum):
    wind_direction = "Wind Direction"
    wave_height = "Wave Height"
    wind_speed = "Wind Speed"
    wind_speed_gust = "Wind Speed Gust"


class MeasurementsAndUnits(TypedDict):
    label: str
    unit: str


FORECAST: dict[ForecastKey, MeasurementsAndUnits] = {
    ForecastKey.wave_height: {"label": "Wave Height", "unit": "feet"},
    ForecastKey.wind_direction: {"label": "Wind Direction", "unit": "degrees"},
    ForecastKey.wind_speed: {"label": "Wind Speed", "unit": "knots"},
    ForecastKey.wind_speed_gust: {"label": "Wind Gust", "unit": "knots"},
}
