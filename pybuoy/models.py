"""Records returned by pybuoy.

A value is ``None`` when the source did not report it.
"""

from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import Any


def _num(source: str, unit: str) -> Any:
    """Declare a numeric field read from ``source`` and measured in ``unit``."""
    return field(
        default=None, metadata={"source": source, "unit": unit, "convert": float}
    )


def _text(source: str) -> Any:
    """Declare a text field read from ``source``."""
    return field(default=None, metadata={"source": source, "convert": str})


@dataclass(frozen=True, slots=True)
class MeteorologicalObservation:
    """Standard meteorological data from one NDBC station report (``txt``)."""

    time: datetime
    """When the observation was made (UTC)."""
    wind_direction: float | None = _num("WDIR", "degT")
    wind_speed: float | None = _num("WSPD", "m/s")
    wind_gust: float | None = _num("GST", "m/s")
    wave_height: float | None = _num("WVHT", "m")
    dominant_wave_period: float | None = _num("DPD", "sec")
    average_wave_period: float | None = _num("APD", "sec")
    wave_direction: float | None = _num("MWD", "degT")
    sea_level_pressure: float | None = _num("PRES", "hPa")
    air_temperature: float | None = _num("ATMP", "degC")
    water_temperature: float | None = _num("WTMP", "degC")
    dewpoint_temperature: float | None = _num("DEWP", "degC")
    visibility: float | None = _num("VIS", "nmi")
    pressure_tendency: float | None = _num("PTDY", "hPa")
    tide: float | None = _num("TIDE", "ft")


@dataclass(frozen=True, slots=True)
class WaveSummaryObservation:
    """Spectral wave summary from one NDBC station report (``spec``)."""

    time: datetime
    """When the observation was made (UTC)."""
    significant_wave_height: float | None = _num("WVHT", "m")
    swell_height: float | None = _num("SwH", "m")
    swell_period: float | None = _num("SwP", "sec")
    wind_wave_height: float | None = _num("WWH", "m")
    wind_wave_period: float | None = _num("WWP", "sec")
    swell_direction: str | None = _text("SwD")
    """Compass point the swell comes from, such as ``"ESE"``."""
    wind_wave_direction: str | None = _text("WWD")
    """Compass point the wind waves come from, such as ``"SSW"``."""
    steepness: str | None = _text("STEEPNESS")
    """NDBC's wave steepness class, such as ``"STEEP"``."""
    average_wave_period: float | None = _num("APD", "sec")
    dominant_wave_direction: float | None = _num("MWD", "degT")


Model = MeteorologicalObservation | WaveSummaryObservation


def units(model: type[Model]) -> dict[str, str]:
    """Return the unit of each numeric field of ``model``, keyed by field name."""
    return {f.name: f.metadata["unit"] for f in fields(model) if "unit" in f.metadata}
