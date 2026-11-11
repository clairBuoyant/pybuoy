"""List of API endpoints pybuoy knows about."""

_FORECASTS_URL = "https://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php"

API_PATH: dict[str, str] = {
    "forecasts": f"{_FORECASTS_URL}",
}
