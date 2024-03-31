"""Mapping key to unit for Observation."""

# https://www.ndbc.noaa.gov/measdes.shtml
from enum import Enum
from typing import TypedDict

NO_NUMERIC_VALUE = "MM"
NO_TEXT_VALUE = "N/A"


class BaseKey(Enum): ...


class ForecastKey(BaseKey):
    wind_direction = "Wind Direction"
    wave_height = "Wave Height"
    wind_speed = "Wind Speed"
    wind_speed_gust = "Wind Speed Gust"


class MeteorologicalKey(BaseKey):
    WDIR = "WDIR"
    WSPD = "WSPD"
    GST = "GST"
    WVHT = "WVHT"
    DPD = "DPD"
    APD = "APD"
    MWD = "MWD"
    PRES = "PRES"
    ATMP = "ATMP"
    WTMP = "WTMP"
    DEWP = "DEWP"
    VIS = "VIS"
    PTDY = "PTDY"
    TIDE = "TIDE"


class WaveSummaryKey(BaseKey):
    WVHT = "WVHT"
    SwH = "SwH"
    SwP = "SwP"
    WWH = "WWH"
    WWP = "WWP"
    SwD = "SwD"
    WWD = "WWD"
    STEEPNESS = "STEEPNESS"
    APD = "APD"
    MWD = "MWD"


class SummaryWaveSteepnessValues(Enum):
    VERY_STEEP = "VERY_STEEP"
    SWELL = "SWELL"
    AVERAGE = "AVERAGE"


class MeasurementsAndUnits(TypedDict):
    label: str
    unit: str


DATE_RECORDED = {
    "#YY": {"label": "Year", "unit": "Y"},
    "MM": {"label": "Month", "unit": "m"},
    "DD": {"label": "Day", "unit": "d"},
    "hh": {"label": "Hour", "unit": "H"},
    "mm": {"label": "Minute", "unit": "M"},
}

# Realtime (dataset="txt")
METEOROLOGICAL: dict[MeteorologicalKey, MeasurementsAndUnits] = {
    MeteorologicalKey.WDIR: {"label": "Wind Direction", "unit": "degrees"},
    MeteorologicalKey.WSPD: {"label": "Wind Speed", "unit": "m/s"},
    MeteorologicalKey.GST: {"label": "Wind Gust", "unit": "m/s"},
    MeteorologicalKey.WVHT: {"label": "Wave Height", "unit": "m"},
    MeteorologicalKey.DPD: {"label": "Dominant Wave Period", "unit": "seconds"},
    MeteorologicalKey.APD: {"label": "Average Wave Period", "unit": "seconds"},
    MeteorologicalKey.MWD: {"label": "Wave Direction", "unit": "degrees"},
    MeteorologicalKey.PRES: {"label": "Sea Level Pressure", "unit": "hPa"},
    MeteorologicalKey.ATMP: {"label": "Air Temperature", "unit": "celcius"},
    MeteorologicalKey.WTMP: {"label": "Water Temperature", "unit": "celcius"},
    MeteorologicalKey.DEWP: {"label": "Dewpoint Temperature", "unit": "celcius"},
    MeteorologicalKey.VIS: {"label": "Visibility", "unit": "nmi"},  # nautical miles
    MeteorologicalKey.PTDY: {
        "label": "Pressure Tendency",
        "unit": "hPa",
    },  # direction +/- amount of pressure change over 3hr period
    MeteorologicalKey.TIDE: {"label": "Tide", "unit": "ft"},
}
# Realtime (dateset="spec")
WAVE_SUMMARY: dict[WaveSummaryKey, MeasurementsAndUnits] = {
    WaveSummaryKey.WVHT: {"label": "Significant Wave Height", "unit": "meters"},
    WaveSummaryKey.SwH: {"label": "Swell Height", "unit": "meters"},
    WaveSummaryKey.SwP: {"label": "Swell Period", "unit": "seconds"},
    WaveSummaryKey.WWH: {"label": "Wind Wave Height", "unit": "meters"},
    WaveSummaryKey.WWP: {"label": "Wind Wave Period", "unit": "seconds"},
    WaveSummaryKey.SwD: {
        "label": "Swell Direction",
        "unit": "string",  # cardinal directions (e.g., SE)
    },
    WaveSummaryKey.WWD: {
        "label": "Wind Wave Direction",
        "unit": "string",  # cardinal directions (e.g., SE)
    },
    WaveSummaryKey.STEEPNESS: {
        "label": "Steepness",
        "unit": "string",  # ? refer to enum class?
    },
    WaveSummaryKey.APD: {"label": "Average Wave Period", "unit": "seconds"},
    WaveSummaryKey.MWD: {
        "label": "Dominant Wave Direction",
        "unit": "degrees",
    },  # direction of waves at dominant period (DPD)
}

FORECAST: dict[ForecastKey, MeasurementsAndUnits] = {
    ForecastKey.wave_height: {"label": "Wave Height", "unit": "feet"},
    ForecastKey.wind_direction: {"label": "Wind Direction", "unit": "degrees"},
    ForecastKey.wind_speed: {"label": "Wind Speed", "unit": "knots"},
    ForecastKey.wind_speed_gust: {"label": "Wind Gust", "unit": "knots"},
}
