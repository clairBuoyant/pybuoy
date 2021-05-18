"""BuoyPy constants."""
from .endpoints import API_PATH  # noqa: F401

__version__ = "0.1.0.dev"


#  Enable users to prepend user_agent
# .format(user_agent)
USER_AGENT_FORMAT = f"{{}} Buoy{__version__}"
