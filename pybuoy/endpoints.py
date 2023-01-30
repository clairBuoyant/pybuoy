"""List of API endpoints pybuoy knows about."""

_BASE_URL = "https://www.ndbc.noaa.gov"
_FORECASTS_URL = "https://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php"

API_PATH: dict[str, str] = {
    "active_stations": f"{_BASE_URL}/activestations",
    "realtime2": f"{_BASE_URL}/data/realtime2",
    "forecasts": f"{_FORECASTS_URL}",
}
