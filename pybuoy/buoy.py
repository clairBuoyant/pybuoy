"""The entry point: one ``Buoy`` gives access to every data source."""

import requests

from pybuoy._http import Client
from pybuoy.forecasts import Forecasts
from pybuoy.realtime import Realtime
from pybuoy.stations import Stations


class Buoy:
    """Gateway to NOAA and NDBC data.

    .. code-block:: python

        from pybuoy import Buoy

        buoy = Buoy()

        observations = buoy.realtime.get("44065")
        stations = buoy.stations.get_active()

    Args:
        timeout: seconds to wait for NOAA or NDBC before giving up.
        session: ``requests`` session to send requests with, for example to
            configure retries or a proxy. A new one is created by default.
    """

    def __init__(
        self, *, timeout: float = 10.0, session: requests.Session | None = None
    ) -> None:
        client = Client(session or requests.Session(), timeout)
        self.realtime = Realtime(client)
        self.stations = Stations(client)
        self.forecasts = Forecasts(client)
