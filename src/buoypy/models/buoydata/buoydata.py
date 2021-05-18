"""Provide the BuoyData class."""
from dataclasses import dataclass
from datetime import date
from .base import BuoyDataBase
from .unit_mapping import WAVE_UNITS, METEOROLOGICAL


@dataclass
class Meteorological:
    date_recorded: date = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["date_recorded"],
    )
    wind_direction: int = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["wind_direction"],
    )
    wind_speed: float = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["wind_speed"],
    )
    wind_gust: float = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["wind_gust"],
    )
    wave_height: float = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["wave_height"],
    )
    dom_wave_period: float = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["dom_wave_period"],
    )
    avg_wave_period: float = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["avg_wave_period"],
    )
    wave_direction: int = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["wave_direction"],
    )
    sea_pressure: float = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["sea_pressure"],
    )
    air_temperature: float = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["air_temperature"],
    )
    water_temperature: float = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["water_temperature"],
    )
    tide: float = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["tide"],
    )
    dewpoint_temperature: float = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["dewpoint_temperature"],
    )
    visibility: float = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["visibility"],
    )
    pressure_tendency: float = BuoyDataBase(
        value=None,
        unit=METEOROLOGICAL["pressure_tendency"],
    )


@dataclass
class Spectral(BuoyDataBase):
    ...


@dataclass
class Wave:
    sea_surface_wave_significant_height: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["sea_surface_wave_significant_height"],
    )  # (m)
    sea_surface_wave_peak_period: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["sea_surface_wave_peak_period"],
    )  # (s)
    sea_surface_wave_mean_period: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["sea_surface_wave_mean_period"],
    )  # (s)
    sea_surface_swell_wave_significant_height: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["sea_surface_swell_wave_significant_height"],
    )  # (m)
    sea_surface_swell_wave_period: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["sea_surface_swell_wave_period"],
    )  # (s)
    sea_surface_wind_wave_significant_height: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["sea_surface_wind_wave_significant_height"],
    )  # (m)
    sea_surface_wind_wave_period: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["sea_surface_wind_wave_period"],
    )  # (s)
    sea_water_temperature: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["sea_surface_wind_wave_period"],
    )  # (c)
    sea_surface_wave_to_direction: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["sea_surface_wind_wave_period"],
    )  # (degree)
    sea_surface_swell_wave_to_direction: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["sea_surface_swell_wave_to_direction"],
    )  # (degree)
    sea_surface_wind_wave_to_direction: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["sea_surface_wind_wave_to_direction"],
    )  # (degree)
    number_of_frequencies: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["number_of_frequencies"],
    )  # (count)
    center_frequencies: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["center_frequencies"],
    )  # (Hz)
    bandwidths: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["bandwidths"],
    )  # (Hz)
    spectral_energy: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["spectral_energy"],
    )  # (m**2/Hz)
    mean_wave_direction: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["mean_wave_direction"],
    )  # (degree)
    principal_wave_direction: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["principal_wave_direction"],
    )  # (degree)
    polar_coordinate_r1: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["polar_coordinate_r1"],
    )  # (1)
    polar_coordinate_r2: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["polar_coordinate_r2"],
    )  # (1)
    calculation_method = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["calculation_method"],
    )  # None,
    sampling_rate: float = BuoyDataBase(
        value=None,
        unit=WAVE_UNITS["sampling_rate"],
    )  # (Hz)


@dataclass
class Wind(BuoyDataBase):
    ...


class BuoyData(Meteorological, Spectral, Wind, Wave):
    # ? in this current state, should the following be the def of buoy/collection
    # ? if yes, then should buoydata be buoydatum... 175-178 only?
    def __init__(
        self,
        meteorological_datum: Meteorological = None,
        spectral_datum: Spectral = None,
        wind_datum: Wind = None,
        wave_datum: Wave = None,
    ):
        super().__init__()
        self._meteorological_data = [meteorological_datum]
        self._spectral_data = [spectral_datum]
        self._wind_data = [wind_datum]
        self._wave_data = [wave_datum]

    @property
    def meteorological_data(self) -> list[Meteorological]:
        return self._meteorological_data

    @property
    def spectral_data(self) -> list[Spectral]:
        return self._spectral_data

    @property
    def wind_data(self) -> list[Wind]:
        return self._wind_data

    @property
    def wave_data(self) -> list[Wave]:
        return self._wave_data

    @meteorological_data.setter
    def meteorological_data(self, met_datum: Meteorological):
        self._meteorological_data.append(met_datum)

    @spectral_data.setter
    def spectral_data(self, spectral_datum: Spectral):
        self._spectral_data.append(spectral_datum)

    @wind_data.setter
    def wind_data(self, wind_datum: Wind):
        self._wind_data.append(wind_datum)

    @wave_data.setter
    def wave_data(self, wave_datum: Wave):
        self._wave_data.append(wave_datum)
