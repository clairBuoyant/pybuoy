from pybuoy.api.base import ApiBase
from pybuoy.const import API_PATH, Endpoints


class Realtime(ApiBase):
    def __init__(self, station_id: str):
        self.station_id = station_id

    # TODO: map phrases like "meterological" to appropriate dataset (i.e., "txt")
    def get(self, dataset="txt"):
        """Get realtime data from the NDBC.

        There are six different data sources:
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
            dataset (str): 'data_spec', 'ocean', 'spec', 'supl', 'swdir', 'swdir2', 'swr1',
                'swr2', or 'txt'.
        """
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

        url = f"{API_PATH[Endpoints.REALTIME.value]}/{self.station_id}.{dataset}"
        return self.parse(self.make_request(url), dataset)
