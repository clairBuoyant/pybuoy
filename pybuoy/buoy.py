from pybuoy.api.forecasts import Forecasts
from pybuoy.api.realtime import Realtime
from pybuoy.api.stations import Stations


class Buoy:
    """Buoy class provides convenient access to NDBC's API.

    Instances of this class are the gateway to interacting with National
    Data Buoy Center (NDBC) through `pybuoy`. The canonical way to get
    an instance of this class is via:

    .. code-block:: python

        from pybuoy import Buoy

        buoy = Buoy() # creates instance to access data from NDBC

        meteorological_data = buoy.realtime.get(station_id="44065")

        all_active_NDBC_stations = buoy.stations.get_active()
    """

    def __init__(self):
        self._forecasts = Forecasts()
        self._realtime = Realtime()
        self._stations = Stations()

    @property
    def forecasts(self) -> Forecasts:
        return self._forecasts

    @property
    def realtime(self) -> Realtime:
        return self._realtime

    @property
    def stations(self) -> Stations:
        return self._stations
