class Observation(float):
    """Observation class encapsulates `Buoy` datum."""

    def __init__(self, value: str, label_and_unit: dict[str, str], datetime=None):
        """Initialize Observation record with relevant metadata.

        Args:
            value (str): recorded weather datum. Defaults to 'MM'.
            label_and_unit (dict[str, str]): label and unit for value.
            datetime (datetime): UTC time of value. Defaults to None.
        """
        self.value = float(value) if value != "MM" else float("nan")
        self._label = label_and_unit["label"]
        self._unit = label_and_unit["unit"]
        self._datetime = datetime

    def __new__(cls, value, *_):
        return float.__new__(cls, value) if value != "MM" else float.__new__(cls, "nan")

    @property
    def datetime(self):
        """Return when this observation was made."""
        return self._datetime

    @property
    def label(self):
        """Return type of observation."""
        return self._label

    @property
    def unit(self):
        """Return this observation's unit."""
        return self._unit

    def __repr__(self):
        return f"Observation({self.label}: {self.__float__()} {self.unit})"

    def __str__(self):
        return f"{self.__float__()} {self.unit}"
