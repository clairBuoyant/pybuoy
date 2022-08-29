from pybuoy import Buoy
from pybuoy.observation import MeteorologicalObservation, WaveSummaryObservation


def test_realtime_meterological_data(test_pybuoy: Buoy):
    example_station_id = "44065"
    response = test_pybuoy.realtime.get(station_id=example_station_id)
    for record in response:
        assert isinstance(record, MeteorologicalObservation)
        assert len(record.__dict__.keys()) == 15


def test_realtime_wave_summary_data(test_pybuoy: Buoy):
    example_station_id = "44065"
    response = test_pybuoy.realtime.get(station_id=example_station_id, dataset="spec")
    for record in response:
        assert isinstance(record, WaveSummaryObservation)
        assert len(record.__dict__.keys()) == 11
