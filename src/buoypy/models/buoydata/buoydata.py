"""Provide the BuoyData class."""
from dataclasses import dataclass
from datetime import date
from .base import BuoyDataBase


@dataclass
class Meteorological:
    date_recorded: date = BuoyDataBase(None)
    wind_direction: int = BuoyDataBase(None)
    wind_speed: float = BuoyDataBase(None)
    wind_gust: float = BuoyDataBase(None)
    wave_height: float = BuoyDataBase(None)
    dom_wave_period: float = BuoyDataBase(None)
    avg_wave_period: float = BuoyDataBase(None)
    wave_direction: int = BuoyDataBase(None)
    sea_pressure: float = BuoyDataBase(None)
    air_temperature: float = BuoyDataBase(None)
    water_temperature: float = BuoyDataBase(None)
    tide: float = BuoyDataBase(None)
    dewpoint_temperature: float = BuoyDataBase(None)
    visibility: float = BuoyDataBase(None)
    pressure_tendency: float = BuoyDataBase(None)


@dataclass
class Spectral(BuoyDataBase):
    ...


@dataclass
class Wave:
    sea_surface_wave_significant_height: float = BuoyDataBase(None)  # (m)
    sea_surface_wave_peak_period: float = BuoyDataBase(None)  # (s)
    sea_surface_wave_mean_period: float = BuoyDataBase(None)  # (s)
    sea_surface_swell_wave_significant_height: float = BuoyDataBase(None)  # (m)
    sea_surface_swell_wave_period: float = BuoyDataBase(None)  # (s)
    sea_surface_wind_wave_significant_height: float = BuoyDataBase(None)  # (m)
    sea_surface_wind_wave_period: float = BuoyDataBase(None)  # (s)
    sea_water_temperature: float = BuoyDataBase(None)  # (c)
    sea_surface_wave_to_direction: float = BuoyDataBase(None)  # (degree)
    sea_surface_swell_wave_to_direction: float = BuoyDataBase(None)  # (degree)
    sea_surface_wind_wave_to_direction: float = BuoyDataBase(None)  # (degree)
    number_of_frequencies: float = BuoyDataBase(None)  # (count)
    center_frequencies: float = BuoyDataBase(None)  # (Hz)
    bandwidths: float = BuoyDataBase(None)  # (Hz)
    spectral_energy: float = BuoyDataBase(None)  # (m**2/Hz)
    mean_wave_direction: float = BuoyDataBase(None)  # (degree)
    principal_wave_direction: float = BuoyDataBase(None)  # (degree)
    polar_coordinate_r1: float = BuoyDataBase(None)  # (1)
    polar_coordinate_r2: float = BuoyDataBase(None)  # (1)
    calculation_method = BuoyDataBase(None)  # None
    sampling_rate: float = BuoyDataBase(None)  # (Hz)


@dataclass
class Wind(BuoyDataBase):
    ...


class BuoyData(Meteorological, Spectral, Wind, Wave):
    def __init__(
        self,
    ):
        super().__init__()
