"""List of API endpoints pybuoy knows about."""

_BASE_URL = "https://www.ndbc.noaa.gov"

API_PATH: dict[str, str] = {
    "active_stations": f"{_BASE_URL}/activestations",
    "realtime2": f"{_BASE_URL}/data/realtime2",
}
