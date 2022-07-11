"""pybuoy constants."""
from enum import Enum

from .endpoints import API_PATH  # noqa: F401

__version__ = "0.2.0"


class Endpoints(Enum):
    ACTIVE_STATIONS = "active_stations"
    REALTIME = "realtime2"


#  Enable users to prepend user_agent
# .format(user_agent)
USER_AGENT_FORMAT = f"{{}} pybuoy-v{__version__}"
