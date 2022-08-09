"""List of API endpoints pybuoy knows about."""

BASE_URL = "https://www.ndbc.noaa.gov"

ACTIVE_STATIONS = "activestations"
REALTIME2 = "realtime2"

API_PATH: dict[str, str] = {
    "active_stations": f"{BASE_URL}/activestations",
    "realtime2": f"{BASE_URL}/data/realtime2",
}
