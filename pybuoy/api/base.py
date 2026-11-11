import requests

from pybuoy.exceptions import NDBCException

REQUEST_TIMEOUT_SECONDS = 10


class ApiBase:
    def make_request(self, url: str, params: dict | None = None) -> str:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
        if response.status_code == 200:
            return response.text
        if response.status_code == 404:
            raise NDBCException(f"No data found at {url}")
        raise ValueError(f"Error code {response.status_code} for url: {url}")
