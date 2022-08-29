from pybuoy.const import NO_VALUE
from pybuoy.unit_mappings import MeasurementsAndUnits, SummaryWaveSteepnessValues


class ObservationFloatDatum(float):
    """Encapsulates `Buoy` datum from `Observation` as float."""

    def __init__(self, value: str, label_unit: MeasurementsAndUnits):
        """Initialize ObservationDatum record with relevant metadata.

        Args:
            value (str): value of observation. (Default: "MM")
            label_unit (MeasurementsAndUnits): label and unit for value.
        """
        self.value = None if value == NO_VALUE else float(value)
        self._label = label_unit["label"]
        self._unit = label_unit["unit"]

    def __new__(cls, value, *_):
        return (
            float.__new__(cls, value)
            if value != NO_VALUE
            else float.__new__(cls, "nan")
        )

    @property
    def label(self):
        """Return type of observation."""
        return self._label

    @property
    def unit(self):
        """Return this observation's unit."""
        return self._unit

    def __repr__(self):
        return f"ObservationDatum({self.label}: {self.__float__()} {self.unit})"

    def __str__(self):
        return f"{self.__float__()} {self.unit}"


class ObservationStringDatum(str):
    """Encapsulates `Buoy` datum from `Observation` as string."""

    def __init__(self, value: str, label_unit: MeasurementsAndUnits):
        """Initialize ObservationDatum record with relevant metadata.

        Args:
            value (str): value of observation. (Default: "MM")
            label_unit (MeasurementsAndUnits): label and unit for value.
        """
        self.value = (
            None
            if value == NO_VALUE or value == SummaryWaveSteepnessValues.NA.value
            else value
        )
        self._label = label_unit["label"]
        self._unit = label_unit["unit"]

    def __new__(cls, value, *_):
        return str.__new__(cls, value)

    @property
    def label(self):
        """Return type of observation."""
        return self._label

    @property
    def unit(self):
        """Return this observation's unit."""
        return self._unit

    def __repr__(self):
        return f"ObservationDatum({self.label}: {self.__str__()})"
