from collections.abc import Mapping
from io import BytesIO
from pathlib import Path
from urllib.parse import parse_qsl

import pytest
import requests
from requests.adapters import BaseAdapter

from pybuoy import Buoy

FIXTURES = Path(__file__).parent / "fixtures"
NDBC_URL = "https://www.ndbc.noaa.gov"
NDFD_URL = "https://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php"


class FakeNoaa(BaseAdapter):
    """Stands in for the NOAA/NDBC services as a ``requests`` transport.

    ``bodies`` maps URL to response text and starts out with the fixtures;
    tests may change it. Unknown URLs answer 404. Set ``status`` to answer
    every request with that status, or ``error`` to fail every request.
    ``calls`` records what was sent.
    """

    realtime_url = f"{NDBC_URL}/data/realtime2/44065.txt"
    stations_url = f"{NDBC_URL}/activestations.xml"
    forecast_url = NDFD_URL

    def __init__(self) -> None:
        super().__init__()
        self.calls: list[dict[str, object]] = []
        self.status: int | None = None
        self.error: requests.RequestException | None = None
        self.bodies = {
            self.realtime_url: _fixture("44065.txt"),
            f"{NDBC_URL}/data/realtime2/44065.spec": _fixture("44065.spec"),
            self.stations_url: _fixture("activestations.xml"),
            self.forecast_url: _fixture("ndfd_forecast.xml"),
        }

    def close(self) -> None:
        pass

    def send(
        self,
        request: requests.PreparedRequest,
        stream: bool = False,
        timeout: float | tuple[float, float] | tuple[float, None] | None = None,
        verify: bool | str = True,
        cert: bytes | str | tuple[bytes | str, bytes | str] | None = None,
        proxies: Mapping[str, str] | None = None,
    ) -> requests.Response:
        url, _, query = (request.url or "").partition("?")
        self.calls.append(
            {"url": url, "params": dict(parse_qsl(query)), "timeout": timeout}
        )
        if self.error is not None:
            raise self.error

        response = requests.Response()
        response.request = request
        response.url = url
        response.encoding = "utf-8"
        response.status_code = self.status or (200 if url in self.bodies else 404)
        response.raw = BytesIO(self.bodies.get(url, "").encode())
        return response


def _fixture(name: str) -> str:
    return (FIXTURES / name).read_text()


@pytest.fixture
def noaa() -> FakeNoaa:
    return FakeNoaa()


@pytest.fixture
def session(noaa: FakeNoaa) -> requests.Session:
    """A session whose every HTTPS request is answered by ``noaa``."""
    session = requests.Session()
    session.mount("https://", noaa)
    return session


@pytest.fixture
def buoy(request: pytest.FixtureRequest, session: requests.Session) -> Buoy:
    """A ``Buoy`` wired to the fake services, or the real ones for ``live`` tests."""
    if request.node.get_closest_marker("live"):
        return Buoy()
    return Buoy(session=session)
