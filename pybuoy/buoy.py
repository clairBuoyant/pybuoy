from pybuoy.api.realtime import Realtime
from pybuoy.api.stations import Stations


class Buoy:
    """Buoy class provides convenient access to NDBC's API.

    Instances of this class are the gateway to interacting with National
    Data Buoy Center (NDBC) through `buoypy`. The canonical way to obtain
    an instance of this class is via:

    .. code-block:: python

        from pybuoy import Buoy

        buoy = Buoy(station_id="44065")
        buoy.realtime.get() # returns last 45 days of meteorological data
    """

    realtime: Realtime
    stations: Stations

    def __init__(self, station_id: str):
        self.realtime = Realtime(station_id=station_id)
        self.stations = Stations()
