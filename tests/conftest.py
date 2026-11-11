from pathlib import Path

import pytest
import requests

from pybuoy import Buoy

FIXTURES = Path(__file__).parent / "fixtures"
NDBC_URL = "https://www.ndbc.noaa.gov"
NDFD_URL = "https://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php"


class FakeNoaa:
    """Stands in for the NOAA/NDBC services.

    ``bodies`` maps URL to response text and starts out with the fixtures;
    tests may change it. Unknown URLs answer 404; known ones answer ``status``.
    ``calls`` records every request so tests can assert on what was sent.
    """

    forecast_url = NDFD_URL

    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []
        self.status = 200
        self.bodies = {
            f"{NDBC_URL}/data/realtime2/44065.txt": _fixture("44065.txt"),
            f"{NDBC_URL}/data/realtime2/44065.spec": _fixture("44065.spec"),
            f"{NDBC_URL}/activestations.xml": _fixture("activestations.xml"),
            NDFD_URL: _fixture("ndfd_forecast.xml"),
        }

    def get(
        self,
        url: str,
        params: dict[str, object] | None = None,
        **request_options: object,
    ) -> "FakeResponse":
        self.calls.append({"url": url, "params": params, **request_options})
        if url not in self.bodies:
            return FakeResponse(404, "")
        return FakeResponse(self.status, self.bodies[url])


class FakeResponse:
    def __init__(self, status_code: int, text: str) -> None:
        self.status_code = status_code
        self.text = text


def _fixture(name: str) -> str:
    return (FIXTURES / name).read_text()


@pytest.fixture(autouse=True)
def noaa(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch) -> FakeNoaa:
    """Replace the network with ``FakeNoaa``, except for tests marked ``live``."""
    fake = FakeNoaa()
    if not request.node.get_closest_marker("live"):
        monkeypatch.setattr(requests, "get", fake.get)
    return fake


@pytest.fixture
def buoy() -> Buoy:
    return Buoy()
