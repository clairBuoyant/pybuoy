from typing import Iterator

from pybuoy.observation import MeteorologicalObservation, WaveSummaryObservation


class Observations:
    """Observations class encapsulates `Observation`s by datetime."""

    def __init__(
        self,
        observations: list[MeteorologicalObservation | WaveSummaryObservation] = None,
    ):
        # TODO: improve error handling
        self._data = observations if observations is not None else []
        self._size = len(self._data)

    @property
    def reports(self) -> list[MeteorologicalObservation | WaveSummaryObservation]:
        return self._data

    @reports.setter
    def reports(
        self, observation: MeteorologicalObservation | WaveSummaryObservation
    ) -> None:
        self._data.append(observation)
        self._size = len(self._data)

    def __getitem__(
        self, key: int
    ) -> MeteorologicalObservation | WaveSummaryObservation:
        return self._data[key]

    def __iter__(self) -> Iterator[MeteorologicalObservation | WaveSummaryObservation]:
        return iter(self._data)

    def __repr__(self) -> str:
        if len(self._data) < 1000:
            return "{}({})".format(
                self.__class__.__name__,
                ", ".join("{}={!r}".format(k, v) for k, v in self.__dict__.items()),
            )
        # Get the first and last three items
        items_to_display = self._data[:3] + self._data[-3:]
        # Find the which item has the longest repr
        max_length_repr = max(items_to_display, key=lambda x: len(repr(x)))
        # Get the length of the item with the longest repr
        padding = len(repr(max_length_repr))
        # Create a list of the reprs of each item and apply the padding
        values = [repr(item).rjust(padding) for item in items_to_display]
        # Insert the '...' inbetween the 3rd and 4th item
        values.insert(3, "...")
        # Convert the list to a string joined by commas
        array_as_string = ", ".join(values)
        return f"Observations([{array_as_string}])"
