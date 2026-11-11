"""NDBC realtime observations.

Format reference: https://www.ndbc.noaa.gov/docs/ndbc_web_data_guide.pdf
"""

from dataclasses import fields
from datetime import UTC, datetime
from typing import Any, Literal, overload

from pybuoy.api.base import ApiBase
from pybuoy.models import MeteorologicalObservation, Observation, WaveSummaryObservation

URL = "https://www.ndbc.noaa.gov/data/realtime2/{station_id}.{dataset}"
MISSING = frozenset({"MM", "N/A"})
TIME_COLUMNS = ("YY", "MM", "DD", "hh", "mm")

# Supporting another dataset means adding its model here and an overload below.
MODELS: dict[str, type[Observation]] = {
    "txt": MeteorologicalObservation,
    "spec": WaveSummaryObservation,
}


class Realtime(ApiBase):
    @overload
    def get(
        self, station_id: str, dataset: Literal["txt"] = "txt"
    ) -> list[MeteorologicalObservation]: ...

    @overload
    def get(
        self, station_id: str, dataset: Literal["spec"]
    ) -> list[WaveSummaryObservation]: ...

    def get(self, station_id: str, dataset: str = "txt") -> list[Any]:
        """Get the last 45 days of observations from a station, newest first.

        Args:
            station_id: NDBC station id, such as ``"44065"``.
            dataset: ``"txt"`` for standard meteorological data or ``"spec"``
                for the spectral wave summary.
        """
        if not station_id:
            raise ValueError("station_id must be provided")
        if dataset not in MODELS:
            raise ValueError(f"dataset must be one of: {', '.join(MODELS)}")

        url = URL.format(station_id=station_id, dataset=dataset)
        return parse_realtime(self.make_request(url), MODELS[dataset])


def parse_realtime[T: Observation](text: str, model: type[T]) -> list[T]:
    """Parse an NDBC realtime file into ``model`` records.

    The first header row names the columns and the second their units.
    Columns the model does not declare are ignored.
    """
    header, _units, *rows = text.splitlines()
    columns = header.lstrip("#").split()
    declared = {f.metadata["source"]: f for f in fields(model) if f.metadata}

    observations = []
    for row in rows:
        cells = dict(zip(columns, row.split(), strict=True))
        year, month, day, hour, minute = (int(cells[c]) for c in TIME_COLUMNS)
        values: dict[str, Any] = {
            f.name: f.metadata["convert"](cells[source])
            for source, f in declared.items()
            if cells.get(source, "MM") not in MISSING
        }
        observations.append(
            model(time=datetime(year, month, day, hour, minute, tzinfo=UTC), **values)
        )
    return observations
