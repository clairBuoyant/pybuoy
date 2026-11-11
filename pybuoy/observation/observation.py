from datetime import datetime

from pybuoy.observation.observation_datum import ObservationFloatDatum
from pybuoy.unit_mappings import FORECAST, NO_NUMERIC_VALUE


class BaseObservation:
    """BaseObservation class for `Buoy` readings by datetime."""

    def __init__(self, datetime: datetime | None = None):
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
            ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items()),
        )

    def __str__(self):
        return f"Observation({self.datetime})"


class ForecastObservation(BaseObservation):
    """Encapsulates forecasted `Buoy` data."""

    def __init__(
        self,
        # TODO: fix dict key type
        values: dict[str, dict],
        datetime: datetime | None = None,
    ):
        super().__init__(datetime=datetime)
        for key in FORECAST:
            new_key = "_".join(FORECAST[key]["label"].lower().split(" "))
            # NDFD marks a missing value with xsi:nil, which arrives here as None.
            value = values.get(key.name, {}).get("value")
            setattr(
                self,
                f"_{new_key}",
                ObservationFloatDatum(
                    NO_NUMERIC_VALUE if value is None else value, FORECAST[key]
                ),
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
