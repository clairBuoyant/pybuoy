from datetime import datetime
from typing import Optional

from pybuoy.observation.observation_datum import (
    ObservationFloatDatum,
    ObservationStringDatum,
)
from pybuoy.unit_mappings import (
    FORECAST,
    METEOROLOGICAL,
    WAVE_SUMMARY,
    MeteorologicalKey,
    WaveSummaryKey,
)

# TODO: support dynamic typing and add slots for efficiency


class BaseObservation:
    """BaseObservation class for `Buoy` readings by datetime."""

    def __init__(self, datetime: Optional[datetime] = None):
        """Initialize BaseObservation record with datetime.

        Args:
            datetime (datetime): UTC time of value. Defaults to None.
        """
        self._datetime = datetime

    @property
    def datetime(self) -> datetime | None:
        """Return when this observation was made."""
        return self._datetime

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join("{}={!r}".format(k, v) for k, v in self.__dict__.items()),
        )

    def __str__(self):
        return f"Observation({self.datetime})"


class MeteorologicalObservation(BaseObservation):
    """Encapsulates `Buoy` meteorological data."""

    def __init__(
        self,
        values: dict[MeteorologicalKey, str],
        datetime: Optional[datetime] = None,
    ):
        """Initialize Observation record with relevant metadata.

        Args:
            values (dict[str,str]): recorded weather data.
            datetime (datetime): UTC time of value. Defaults to None.
        """
        super().__init__(datetime=datetime)

        for key in METEOROLOGICAL:
            new_key = "_".join(METEOROLOGICAL[key]["label"].lower().split(" "))
            setattr(
                self,
                f"_{new_key}",
                ObservationStringDatum(values[key], METEOROLOGICAL[key]),
            ) if METEOROLOGICAL[key]["unit"] == "string" else setattr(
                self,
                f"_{new_key}",
                ObservationFloatDatum(values[key], METEOROLOGICAL[key]),
            )

    @property
    def wind_direction(self) -> ObservationFloatDatum:
        """Return observed wind direction."""
        return self._wind_direction  # type: ignore # this is dynamically set

    @property
    def wind_speed(self) -> ObservationFloatDatum:
        """Return observed wind speed."""
        return self._wind_speed  # type: ignore # this is dynamically set

    @property
    def wind_gust(self) -> ObservationFloatDatum:
        """Return observed wind gust."""
        return self._wind_gust  # type: ignore # this is dynamically set

    @property
    def wave_height(self) -> ObservationFloatDatum:
        """Return observed wave height."""
        return self._wave_height  # type: ignore # this is dynamically set

    @property
    def dominant_wave_period(self) -> ObservationFloatDatum:
        """Return observed dominant wave period."""
        return self._dominant_wave_period  # type: ignore # this is dynamically set

    @property
    def average_wave_period(self) -> ObservationFloatDatum:
        """Return observed average wave period."""
        return self._average_wave_period  # type: ignore # this is dynamically set

    @property
    def wave_direction(self) -> ObservationFloatDatum:
        """Return observed wave direction."""
        return self._wave_direction  # type: ignore # this is dynamically set

    @property
    def sea_level_pressure(self) -> ObservationFloatDatum:
        """Return observed sea level pressure."""
        return self._sea_level_pressure  # type: ignore # this is dynamically set

    @property
    def air_temperature(self) -> ObservationFloatDatum:
        """Return observed air temperature."""
        return self._air_temperature  # type: ignore # this is dynamically set

    @property
    def water_temperature(self) -> ObservationFloatDatum:
        """Return observed water temperature."""
        return self._water_temperature  # type: ignore # this is dynamically set

    @property
    def dewpoint_temperature(self) -> ObservationFloatDatum:
        """Return observed dewpoint temperature."""
        return self._dewpoint_temperature  # type: ignore # this is dynamically set

    @property
    def visibility(self) -> ObservationFloatDatum:
        """Return observed visibility."""
        return self._visibility  # type: ignore # this is dynamically set

    @property
    def pressure_tendency(self) -> ObservationFloatDatum:
        """Return observed pressure tendency."""
        return self._pressure_tendency  # type: ignore # this is dynamically set

    @property
    def tide(self) -> ObservationFloatDatum:
        """Return observed tide."""
        return self._tide  # type: ignore # this is dynamically set


class WaveSummaryObservation(BaseObservation):
    """Encapsulates `Buoy` wave summary data."""

    def __init__(
        self,
        values: dict[WaveSummaryKey, str],
        datetime: Optional[datetime] = None,
    ):
        """Initialize Observation record with relevant metadata.

        Args:
            values (dict[str,str]): recorded weather data.
            datetime (datetime): UTC time of value. Defaults to None.
        """
        super().__init__(datetime=datetime)

        for key in WAVE_SUMMARY:
            new_key = "_".join(WAVE_SUMMARY[key]["label"].lower().split(" "))
            setattr(
                self,
                f"_{new_key}",
                ObservationStringDatum(values[key], WAVE_SUMMARY[key]),
            ) if WAVE_SUMMARY[key]["unit"] == "string" else setattr(
                self,
                f"_{new_key}",
                ObservationFloatDatum(values[key], WAVE_SUMMARY[key]),
            )

    @property
    def significant_wave_height(self) -> ObservationFloatDatum:
        """Return observed wave height."""
        return self._significant_wave_height  # type: ignore # this is dynamically set

    @property
    def swell_height(self) -> ObservationFloatDatum:
        """Return observed swell height."""
        return self._swell_height  # type: ignore # this is dynamically set

    @property
    def swell_period(self) -> ObservationFloatDatum:
        """Return observed swell period."""
        return self._swell_period  # type: ignore # this is dynamically set

    @property
    def wind_wave_height(self) -> ObservationFloatDatum:
        """Return observed wind wave height."""
        return self._wind_wave_height  # type: ignore # this is dynamically set

    @property
    def wind_wave_period(self) -> ObservationFloatDatum:
        """Return observed wind wave period."""
        return self._wind_wave_period  # type: ignore # this is dynamically set

    @property
    def swell_direction(self) -> ObservationStringDatum:
        """Return observed swell direction."""
        return self._swell_direction  # type: ignore # this is dynamically set

    @property
    def wind_wave_direction(self) -> ObservationStringDatum:
        """Return observed wind wave direction."""
        return self._wind_wave_direction  # type: ignore # this is dynamically set

    @property
    def steepness(self) -> ObservationStringDatum:
        """Return observed wave steepness."""
        return self._steepness  # type: ignore # this is dynamically set

    @property
    def average_wave_period(self) -> ObservationFloatDatum:
        """Return observed average wave period."""
        return self._average_wave_period  # type: ignore # this is dynamically set

    @property
    def dominant_wave_direction(self) -> ObservationFloatDatum:
        """Return observed direction of waves at dominant period."""
        return self._dominant_wave_direction  # type: ignore # this is dynamically set


class ForecastObservation(BaseObservation):
    """Encapsulates forecasted `Buoy` data."""

    def __init__(
        self,
        # TODO: fix dict key type
        values: dict[str, dict],
        datetime: Optional[datetime] = None,
    ):
        super().__init__(datetime=datetime)
        for key in FORECAST:
            new_key = "_".join(FORECAST[key]["label"].lower().split(" "))
            default_val = {"value": "nan"}  # TODO: refactor
            value = values.get(key.name, default_val)
            value_value = value.get("value", "nan")  # TODO: rename
            setattr(
                self,
                f"_{new_key}",
                ObservationFloatDatum(value_value, FORECAST[key]),
            )

    def __str__(self):
        return f"Prediction({self.datetime})"

    @property
    def wind_direction(self) -> ObservationFloatDatum:
        """Return observed wind direction."""
        return self._wind_direction  # type: ignore # this is dynamically set

    @property
    def wind_speed(self) -> ObservationFloatDatum:
        """Return observed wind speed."""
        return self._wind_speed  # type: ignore # this is dynamically set

    @property
    def wind_gust(self) -> ObservationFloatDatum:
        """Return observed wind gust."""
        return self._wind_gust  # type: ignore # this is dynamically set

    @property
    def wave_height(self) -> ObservationFloatDatum:
        """Return observed wave height."""
        return self._wave_height  # type: ignore # this is dynamically set
