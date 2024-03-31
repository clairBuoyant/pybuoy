from typing import Literal, overload

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

    # TODO: consider mapping str literal to dataset
    def get(
        self,
        station_id: str,
        dataset: RealtimeDatasetsValues = RealtimeDatasets.txt.value,
    ):
        """Get realtime data from the NDBC.

        There are nine different data sources:
            - data_spec     Raw Spectral Wave Data
            - ocean         Oceanographic Data
            - spec          Spectral Wave Summary Data
            - supl          Supplemental Measurements Data
            - swdir         Spectral Wave Data (alpha1)
            - swdir2        Spectral Wave Data (alpha2)
            - swr1          Spectral Wave Data (r1)
            - swr2          Spectral Wave Data (r2)
            - txt           Standard Meteorological Data

        Args:
            buoy_id (str): id of buoy
            dataset (str): one of the aforementioned data sources
        """
        if not station_id:
            raise ValueError("station_id must be provided")

        dataset_options = {
            "data_spec",
            "ocean",
            "spec",
            "supl",
            "swdir",
            "swdir2",
            "swr1",
            "swr2",
            "txt",
        }

        if dataset not in dataset_options:
            raise ValueError(f"Dataset must be one of {', '.join(dataset_options)}")

        url = f"{API_PATH[Endpoints.REALTIME.value]}/{station_id}.{dataset}"

        return self.parse(data=self.make_request(url), dataset=dataset)
