"""HTTP access to NOAA and NDBC."""

from collections.abc import Mapping

import requests

from pybuoy.errors import RequestError

# The largest answer is about 0.6 MB (45 days of observations from one station).
_MAX_MEGABYTES = 16


class Client:
    """Fetches text over HTTP, raising ``RequestError`` for any failure."""

    def __init__(self, session: requests.Session, timeout: float) -> None:
        self._session = session
        self._timeout = timeout

    def get(self, url: str, params: Mapping[str, str | float] | None = None) -> str:
        """Return the body of a 200 answer from ``url`` as text."""
        body = bytearray()
        # Assumed when no charset is declared, as for NDBC's station list, which
        # requests would read as Latin-1. Both services write UTF-8 or ASCII.
        charset = "utf-8"
        status: int | None = None
        try:
            with self._session.get(
                url, params=params, timeout=self._timeout, stream=True
            ) as response:
                status = response.status_code
                if "charset" in response.headers.get("Content-Type", "").lower():
                    charset = response.encoding or charset
                # Read in pieces so an oversized answer is refused, not loaded.
                # An error answer is read too, so its connection can be reused.
                for chunk in response.iter_content(chunk_size=64 * 1024):
                    body += chunk
                    if len(body) > _MAX_MEGABYTES * 1024 * 1024:
                        raise RequestError(
                            f"{url} sent more than {_MAX_MEGABYTES} MB", status
                        )
                if status != 200:
                    raise RequestError(f"{url} answered with status {status}", status)
        except requests.RequestException as error:
            raise RequestError(f"Request to {url} failed: {error}", status) from error
        try:
            return body.decode(charset, errors="replace")
        except (LookupError, UnicodeError):  # a charset Python cannot decode
            return body.decode(errors="replace")
