import requests

from pybuoy.exceptions import NDBCException
from pybuoy.mixins.parser import ParserMixin

REQUEST_TIMEOUT_SECONDS = 10


class ApiBase(ParserMixin):
    def make_request(self, url: str, params: dict | None = None) -> str:
        """Get ``url`` and return the body of a 200 answer.

        Raises:
            NDBCException: the answer was 404.
            ValueError: the answer was any other status.
        """
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
        if response.status_code == 200:
            return response.text
        if response.status_code == 404:
            raise NDBCException(f"No data found at {url}")
        raise ValueError(f"Error code {response.status_code} for url: {url}")
