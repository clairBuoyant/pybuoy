import gzip
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.metadata import version
from threading import Thread

import pytest
import requests
from conftest import FakeNoaa

import pybuoy
from pybuoy import Buoy, PybuoyError, RequestError, StationNotFoundError
from pybuoy._http import Client


class LocalServer(BaseHTTPRequestHandler):
    """A real HTTP server on the loopback interface.

    The fake transport stops short of the connection pool and of compressed
    bodies; this answers ``/found`` with a gzip body and anything else with 404.
    """

    protocol_version = "HTTP/1.1"
    connections = 0

    def setup(self) -> None:
        super().setup()
        LocalServer.connections += 1

    def do_GET(self) -> None:
        found = self.path == "/found"
        body = gzip.compress("naïve".encode()) if found else b"no such file"
        self.send_response(200 if found else 404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        if found:
            self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *values: object) -> None:
        pass


@pytest.fixture
def local_url() -> Iterator[str]:
    LocalServer.connections = 0
    server = ThreadingHTTPServer(("127.0.0.1", 0), LocalServer)
    Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    server.server_close()


@pytest.fixture
def client() -> Iterator[Client]:
    with requests.Session() as session:
        session.trust_env = False  # no proxy between the test and the loopback
        yield Client(session, timeout=5.0)


def test_connection_is_reused_after_an_error_status(
    client: Client, local_url: str
) -> None:
    for _ in range(3):
        with pytest.raises(RequestError, match="404"):
            client.get(f"{local_url}/missing")

    assert LocalServer.connections == 1


def test_compressed_answer_is_decoded(client: Client, local_url: str) -> None:
    assert client.get(f"{local_url}/found") == "naïve"


def test_requests_time_out_after_ten_seconds_by_default(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    buoy.stations.get_active()

    assert noaa.calls[0]["timeout"] == 10.0


def test_timeout_is_configurable(session: requests.Session, noaa: FakeNoaa) -> None:
    Buoy(timeout=3.0, session=session).stations.get_active()

    assert noaa.calls[0]["timeout"] == 3.0


def test_error_status_raises_request_error(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.status = 503

    with pytest.raises(RequestError, match="503") as raised:
        buoy.stations.get_active()

    assert raised.value.status == 503


def test_transport_failure_raises_request_error(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.error = requests.ConnectionError("connection refused")

    with pytest.raises(RequestError, match="connection refused") as raised:
        buoy.stations.get_active()

    assert raised.value.status is None
    assert raised.value.__cause__ is noaa.error


def test_answer_larger_than_16_mb_raises_request_error(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    noaa.bodies[noaa.stations_url] = "x" * (16 * 1024 * 1024 + 1)

    with pytest.raises(RequestError, match="more than 16 MB") as raised:
        buoy.stations.get_active()

    assert raised.value.status == 200


def test_answer_of_exactly_16_mb_is_accepted(buoy: Buoy, noaa: FakeNoaa) -> None:
    stations = noaa.bodies[noaa.stations_url]
    noaa.bodies[noaa.stations_url] = stations.ljust(16 * 1024 * 1024)

    assert len(buoy.stations.get_active()) == 4


def test_failure_while_reading_the_body_raises_request_error(
    buoy: Buoy, noaa: FakeNoaa
) -> None:
    noaa.read_error = requests.exceptions.ChunkedEncodingError("connection broken")

    with pytest.raises(RequestError, match="connection broken") as raised:
        buoy.stations.get_active()

    assert raised.value.__cause__ is noaa.read_error


def test_declared_charset_is_honoured(buoy: Buoy, noaa: FakeNoaa) -> None:
    # NDBC declares ISO-8859-1 for its realtime files.
    noaa.encoding = "latin-1"
    noaa.bodies[noaa.spec_url] = noaa.bodies[noaa.spec_url].replace("ESE", "ÉSE")

    assert buoy.realtime.get("44065", "spec")[0].swell_direction == "ÉSE"


def test_charset_is_found_whatever_its_case(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.encoding = "latin-1"
    noaa.content_types[noaa.stations_url] = "text/xml; Charset=ISO-8859-1"
    noaa.bodies[noaa.stations_url] = noaa.bodies[noaa.stations_url].replace(
        "5N 95W", "Añasco"
    )

    assert buoy.stations.get_active()[1].name == "Añasco"


@pytest.mark.parametrize("charset", ["klingon", "idna", "undefined"])
def test_charset_python_cannot_decode_is_read_as_utf_8(
    buoy: Buoy, noaa: FakeNoaa, charset: str
) -> None:
    noaa.content_types[noaa.stations_url] = f"text/xml; charset={charset}"

    assert len(buoy.stations.get_active()) == 4


def test_bytes_that_are_not_utf_8_are_replaced(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.encoding = "latin-1"
    noaa.bodies[noaa.stations_url] = noaa.bodies[noaa.stations_url].replace(
        "5N 95W", "Añasco"
    )

    assert buoy.stations.get_active()[1].name == "A\N{REPLACEMENT CHARACTER}asco"


def test_unknown_station_raises_station_not_found(buoy: Buoy) -> None:
    with pytest.raises(StationNotFoundError, match="'txt' data for station 'ZZZZZ'"):
        buoy.realtime.get("ZZZZZ")


def test_other_realtime_failures_are_request_errors(buoy: Buoy, noaa: FakeNoaa) -> None:
    noaa.status = 500

    with pytest.raises(RequestError, match="500"):
        buoy.realtime.get("44065")


@pytest.mark.parametrize("error", [RequestError, StationNotFoundError])
def test_every_error_is_a_pybuoy_error(error: type[Exception]) -> None:
    assert issubclass(error, PybuoyError)


def test_version_comes_from_the_installed_package() -> None:
    assert pybuoy.__version__ == version("pybuoy")
