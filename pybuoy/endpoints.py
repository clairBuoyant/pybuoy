"""List of API endpoints buoy-py knows about."""

BASE_URL = "https://www.ndbc.noaa.gov"

API_PATH: dict[str, str] = {
    "active_stations": f"{BASE_URL}/activestations",
    "realtime2": f"{BASE_URL}/data/realtime2",
}
