class Observation(float):
    """TBD."""

    def __init__(self, value, label_and_unit, datetime=None):
        self.value = value
        self._label = label_and_unit["label"]
        self._unit = label_and_unit["unit"]
        self._datetime = datetime

    def __new__(cls, value, *_):
        # TODO: improve handling of missing values - currently defaults to -1
        return float.__new__(cls, value) if value != "MM" else float.__new__(cls, "-1")

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
