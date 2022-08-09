"""pybuoy constants."""
from .endpoints import ACTIVE_STATIONS, API_PATH, REALTIME2  # noqa: F401

__version__ = "0.2.0"

#  Enable users to prepend user_agent
# .format(user_agent)
USER_AGENT_FORMAT = f"{{}} pybuoy-v{__version__}"
