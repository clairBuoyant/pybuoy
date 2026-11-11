"""HTTP access to NOAA and NDBC."""

from collections.abc import Mapping

import requests

from pybuoy.errors import RequestError


class Client:
    """Fetches text over HTTP, raising ``RequestError`` for any failure."""

    def __init__(self, session: requests.Session, timeout: float) -> None:
        self._session = session
        self._timeout = timeout

    def get(self, url: str, params: Mapping[str, str | float] | None = None) -> str:
        try:
            response = self._session.get(url, params=params, timeout=self._timeout)
        except requests.RequestException as error:
            raise RequestError(f"Could not reach {url}: {error}") from error
        if response.status_code != 200:
            raise RequestError(
                f"{url} answered with status {response.status_code}",
                status=response.status_code,
            )
        return response.text
