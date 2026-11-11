from typing import Literal, get_args, overload

from pybuoy.api.base import ApiBase
from pybuoy.const import API_PATH, Endpoints, RealtimeDatasets, RealtimeDatasetsValues
from pybuoy.observation.observations import (
    MeteorologicalObservations,
    WaveSummaryObservations,
)


class Realtime(ApiBase):
    @overload
    def get(
        self,
        station_id: str,
        dataset: Literal["spec"],
    ) -> WaveSummaryObservations: ...

    @overload
    def get(
        self, station_id: str, dataset: Literal["txt"] = "txt"
    ) -> MeteorologicalObservations: ...

    def get(
        self,
        station_id: str,
        dataset: RealtimeDatasetsValues = RealtimeDatasets.txt.value,
    ):
        """Get realtime data from the NDBC.

        Supported datasets:
            - spec          Spectral Wave Summary Data
            - txt           Standard Meteorological Data

        Args:
            station_id (str): id of buoy
            dataset (str): one of the aforementioned datasets
        """
        if not station_id:
            raise ValueError("station_id must be provided")

        dataset_options = get_args(RealtimeDatasetsValues)
        if dataset not in dataset_options:
            raise ValueError(f"Dataset must be one of: {', '.join(dataset_options)}")

        url = f"{API_PATH[Endpoints.REALTIME.value]}/{station_id}.{dataset}"

        return self.parse(data=self.make_request(url), dataset=dataset)
