from pathlib import Path

import pytest
import requests

from pybuoy import Buoy

FIXTURES = Path(__file__).parent / "fixtures"

NDBC_URL = "https://www.ndbc.noaa.gov"
NDFD_URL = "https://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php"

ROUTES = {
    f"{NDBC_URL}/data/realtime2/44065.txt": "44065.txt",
    f"{NDBC_URL}/data/realtime2/44065.spec": "44065.spec",
    f"{NDBC_URL}/activestations.xml": "activestations.xml",
    NDFD_URL: "ndfd_forecast.xml",
}


class FakeResponse:
    def __init__(self, status_code: int, text: str) -> None:
        self.status_code = status_code
        self.text = text


@pytest.fixture(autouse=True)
def noaa(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    """Serve fixtures instead of the network, except for tests marked ``live``.

    Returns the list of requests made, so tests can assert on what was sent.
    """
    calls: list[dict] = []
    if request.node.get_closest_marker("live"):
        return calls

    def fake_get(
        url: str, params: dict | None = None, **kwargs: object
    ) -> FakeResponse:
        calls.append({"url": url, "params": params, **kwargs})
        name = ROUTES.get(url)
        if name is None:
            return FakeResponse(404, "")
        return FakeResponse(200, (FIXTURES / name).read_text())

    monkeypatch.setattr(requests, "get", fake_get)
    return calls


@pytest.fixture
def buoy() -> Buoy:
    return Buoy()
