"""Provide the BuoyData class."""
from dataclasses import dataclass
from datetime import date
from .base import BuoyDataBase
from .unit_mapping import WAVE_UNITS, METEOROLOGICAL


@dataclass
class Meteorological:
    date_recorded: date = BuoyDataBase(
        None,
        METEOROLOGICAL["date_recorded"],
    )
    wind_direction: int = BuoyDataBase(
        None,
        METEOROLOGICAL["wind_direction"],
    )
    wind_speed: float = BuoyDataBase(
        None,
        METEOROLOGICAL["wind_speed"],
    )
    wind_gust: float = BuoyDataBase(
        None,
        METEOROLOGICAL["wind_gust"],
    )
    wave_height: float = BuoyDataBase(
        None,
        METEOROLOGICAL["wave_height"],
    )
    dom_wave_period: float = BuoyDataBase(
        None,
        METEOROLOGICAL["dom_wave_period"],
    )
    avg_wave_period: float = BuoyDataBase(
        None,
        METEOROLOGICAL["avg_wave_period"],
    )
    wave_direction: int = BuoyDataBase(
        None,
        METEOROLOGICAL["wave_direction"],
    )
    sea_pressure: float = BuoyDataBase(
        None,
        METEOROLOGICAL["sea_pressure"],
    )
    air_temperature: float = BuoyDataBase(
        None,
        METEOROLOGICAL["air_temperature"],
    )
    water_temperature: float = BuoyDataBase(
        None,
        METEOROLOGICAL["water_temperature"],
    )
    tide: float = BuoyDataBase(
        None,
        METEOROLOGICAL["tide"],
    )
    dewpoint_temperature: float = BuoyDataBase(
        None,
        METEOROLOGICAL["dewpoint_temperature"],
    )
    visibility: float = BuoyDataBase(
        None,
        METEOROLOGICAL["visibility"],
    )
    pressure_tendency: float = BuoyDataBase(
        None,
        METEOROLOGICAL["pressure_tendency"],
    )


@dataclass
class Spectral(BuoyDataBase):
    ...


@dataclass
class Wave:
    sea_surface_wave_significant_height: float = BuoyDataBase(
        None,
        WAVE_UNITS["sea_surface_wave_significant_height"],
    )  # (m)
    sea_surface_wave_peak_period: float = BuoyDataBase(
        None,
        WAVE_UNITS["sea_surface_wave_peak_period"],
    )  # (s)
    sea_surface_wave_mean_period: float = BuoyDataBase(
        None,
        WAVE_UNITS["sea_surface_wave_mean_period"],
    )  # (s)
    sea_surface_swell_wave_significant_height: float = BuoyDataBase(
        None,
        WAVE_UNITS["sea_surface_swell_wave_significant_height"],
    )  # (m)
    sea_surface_swell_wave_period: float = BuoyDataBase(
        None,
        WAVE_UNITS["sea_surface_swell_wave_period"],
    )  # (s)
    sea_surface_wind_wave_significant_height: float = BuoyDataBase(
        None,
        WAVE_UNITS["sea_surface_wind_wave_significant_height"],
    )  # (m)
    sea_surface_wind_wave_period: float = BuoyDataBase(
        None,
        WAVE_UNITS["sea_surface_wind_wave_period"],
    )  # (s)
    sea_water_temperature: float = BuoyDataBase(
        None,
        WAVE_UNITS["sea_surface_wind_wave_period"],
    )  # (c)
    sea_surface_wave_to_direction: float = BuoyDataBase(
        None,
        WAVE_UNITS["sea_surface_wind_wave_period"],
    )  # (degree)
    sea_surface_swell_wave_to_direction: float = BuoyDataBase(
        None,
        WAVE_UNITS["sea_surface_swell_wave_to_direction"],
    )  # (degree)
    sea_surface_wind_wave_to_direction: float = BuoyDataBase(
        None,
        WAVE_UNITS["sea_surface_wind_wave_to_direction"],
    )  # (degree)
    number_of_frequencies: float = BuoyDataBase(
        None,
        WAVE_UNITS["number_of_frequencies"],
    )  # (count)
    center_frequencies: float = BuoyDataBase(
        None,
        WAVE_UNITS["center_frequencies"],
    )  # (Hz)
    bandwidths: float = BuoyDataBase(
        None,
        WAVE_UNITS["bandwidths"],
    )  # (Hz)
    spectral_energy: float = BuoyDataBase(
        None,
        WAVE_UNITS["spectral_energy"],
    )  # (m**2/Hz)
    mean_wave_direction: float = BuoyDataBase(
        None,
        WAVE_UNITS["mean_wave_direction"],
    )  # (degree)
    principal_wave_direction: float = BuoyDataBase(
        None,
        WAVE_UNITS["principal_wave_direction"],
    )  # (degree)
    polar_coordinate_r1: float = BuoyDataBase(
        None,
        WAVE_UNITS["polar_coordinate_r1"],
    )  # (1)
    polar_coordinate_r2: float = BuoyDataBase(
        None,
        WAVE_UNITS["polar_coordinate_r2"],
    )  # (1)
    calculation_method = BuoyDataBase(
        None,
        WAVE_UNITS["calculation_method"],
    )  # None,
    sampling_rate: float = BuoyDataBase(
        None,
        WAVE_UNITS["sampling_rate"],
    )  # (Hz)


@dataclass
class Wind(BuoyDataBase):
    ...


class BuoyData(Meteorological, Spectral, Wind, Wave):
    def __init__(
        self,
    ):
        super().__init__()
