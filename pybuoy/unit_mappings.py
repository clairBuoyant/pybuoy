"""Mapping key to unit for Observation."""
# https://www.ndbc.noaa.gov/measdes.shtml
from enum import Enum
from typing import TypedDict

NO_NUMERIC_VALUE = "MM"
NO_TEXT_VALUE = "N/A"


class BaseKey(Enum):
    ...


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


# TODO: update below for dynamic mapping

WAVE_UNITS = {
    "sea_surface_wave_significant_height": "meters",
    "sea_surface_wave_peak_period": "seconds",
    "sea_surface_wave_mean_period": "seconds",
    "sea_surface_swell_wave_significant_height": "meters",
    "sea_surface_swell_wave_period": "seconds",
    "sea_surface_wind_wave_significant_height": "meters",
    "sea_surface_wind_wave_period": "seconds",
    "sea_water_temperature": "celcius",
    "sea_surface_wave_to_direction": "degrees",
    "sea_surface_swell_wave_to_direction": "degrees",
    "sea_surface_wind_wave_to_direction": "degrees",
    "number_of_frequencies": "count",
    "center_frequencies": "Hz",
    "bandwidths": "Hz",
    "spectral_energy": "m**2/Hz",
    "mean_wave_direction": "degrees",
    "principal_wave_direction": "degrees",
    "polar_coordinate_r1": "1",
    "polar_coordinate_r2": "1",
    "calculation_method": None,
    "sampling_rate": "Hz",
}

CURRENT_UNITS = {
    "bin": "count",
    "depth": "meters",
    "direction_of_sea_water_velocity": "degrees",
    "sea_water_speed": "c/s",
    "upward_sea_water_velocity": "c/s",
    "error_velocity": "c/s",
    "platform_orientation": "degrees",
    "platform_pitch_angle": "degrees",
    "platform_roll_angle": "degrees",
    "sea_water_temperature": "celcius",
    "pct_good_3_beam": "percent",
    "pct_good_4_beam": "percent",
    "pct_rejected": "percent",
    "pct_bad": "percent",
    "echo_intensity_beam1": "count",
    "echo_intensity_beam2": "count",
    "echo_intensity_beam3": "count",
    "echo_intensity_beam4": "count",
    "correlation_magnitude_beam1": "count",
    "correlation_magnitude_beam2": "count",
    "correlation_magnitude_beam3": "count",
    "correlation_magnitude_beam4": "count",
    "quality_flags": None,
}

WIND_UNITS = {
    "wind_from_direction": "degrees",
    "wind_speed": "m/s",
    "wind_speed_of_gust": "m/s",
    "upward_air_velocity": "m/s",
}

# REALTIME_WAVE_UNITS = {}

# SPECTRAL_UNITS = {}
