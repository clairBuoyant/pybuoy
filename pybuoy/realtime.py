"""NDBC realtime observations.

Format reference: https://www.ndbc.noaa.gov/docs/ndbc_web_data_guide.pdf
"""

from dataclasses import fields
from datetime import UTC, datetime
from typing import Any, Literal, overload

from pybuoy._http import Client
from pybuoy.errors import RequestError, StationNotFoundError, _parser
from pybuoy.models import MeteorologicalObservation, Observation, WaveSummaryObservation

_URL = "https://www.ndbc.noaa.gov/data/realtime2/{station_id}.{dataset}"
# NDBC writes MM for a value it does not have, N/A for a missing steepness
# and -99 for a missing wave direction in the spectral wave summary.
_MISSING = frozenset({"MM", "N/A", "-99"})
_TIME_COLUMNS = ["YY", "MM", "DD", "hh", "mm"]

# Supporting another dataset means adding its model here and an overload below.
_MODELS: dict[str, type[Observation]] = {
    "txt": MeteorologicalObservation,
    "spec": WaveSummaryObservation,
}


class Realtime:
    def __init__(self, client: Client) -> None:
        self._client = client

    @overload
    def get(
        self, station_id: str | int, dataset: Literal["txt"] = "txt"
    ) -> list[MeteorologicalObservation]: ...

    @overload
    def get(
        self, station_id: str | int, dataset: Literal["spec"]
    ) -> list[WaveSummaryObservation]: ...

    def get(self, station_id: str | int, dataset: str = "txt") -> list[Any]:
        """Get the last 45 days of observations from a station, newest first.

        Args:
            station_id: NDBC station id, such as ``"44065"`` or ``"burl1"``.
            dataset: ``"txt"`` for standard meteorological data or ``"spec"``
                for the spectral wave summary.
        """
        # NDBC file names are upper case and its paths are case-sensitive.
        station_id = str(station_id).upper()
        if not station_id.isalnum():
            raise ValueError("station_id must be letters and digits, such as '44065'")
        if dataset not in _MODELS:
            raise ValueError(f"dataset must be one of: {', '.join(_MODELS)}")

        url = _URL.format(station_id=station_id, dataset=dataset)
        try:
            body = self._client.get(url)
        except RequestError as error:
            if error.status == 404:
                raise StationNotFoundError(
                    f"NDBC has no {dataset!r} data for station {station_id!r}"
                ) from error
            raise
        return parse_realtime(body, _MODELS[dataset])


@_parser
def parse_realtime[T: Observation](text: str, model: type[T]) -> list[T]:
    """Parse an NDBC realtime file into ``model`` records.

    The first header row names the columns and the second their units.
    Columns the model does not declare are ignored.
    """
    header, _units, *rows = text.splitlines()
    columns = header.lstrip("#").split()
    if columns[: len(_TIME_COLUMNS)] != _TIME_COLUMNS:
        raise ValueError(f"not an NDBC realtime file: it starts with {header!r}")
    declared = {f.metadata["source"]: f for f in fields(model) if f.metadata}

    observations = []
    for row in rows:
        cells = dict(zip(columns, row.split(), strict=True))
        year, month, day, hour, minute = (int(cells[c]) for c in _TIME_COLUMNS)
        values: dict[str, Any] = {
            f.name: f.metadata["convert"](cells[source])
            for source, f in declared.items()
            if cells.get(source, "MM") not in _MISSING
        }
        observations.append(
            model(time=datetime(year, month, day, hour, minute, tzinfo=UTC), **values)
        )
    return observations
