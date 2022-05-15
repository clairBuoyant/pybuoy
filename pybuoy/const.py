"""BuoyPy constants."""
from enum import Enum

from .endpoints import API_PATH  # noqa: F401

__version__ = "v0.1.1_dev"


class Endpoints(Enum):
    ACTIVE_STATIONS = "active_stations"
    REALTIME = "realtime2"


#  Enable users to prepend user_agent
# .format(user_agent)
USER_AGENT_FORMAT = f"{{}} Buoy{__version__}"
