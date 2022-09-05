from datetime import datetime
from random import randrange

from pybuoy import Buoy
from pybuoy.observation import MeteorologicalObservation, WaveSummaryObservation

# TODO: check values to ensure float and str are set as expected
example_station_id = "44065"


def test_realtime_meterological_data(test_pybuoy: Buoy):
    response = test_pybuoy.realtime.get(station_id=example_station_id)
    for record in response:
        assert isinstance(record, MeteorologicalObservation)
        assert len(record.__dict__.keys()) == 15

    random_record = response[randrange(len(response.reports))]

    assert (
        hasattr(random_record, "datetime") and type(random_record.datetime) is datetime
    )
    assert hasattr(random_record, "wind_direction")
    assert hasattr(random_record, "wind_speed")
    assert hasattr(random_record, "wind_gust")
    assert hasattr(random_record, "wave_height")
    assert hasattr(random_record, "dominant_wave_period")
    assert hasattr(random_record, "average_wave_period")
    assert hasattr(random_record, "wave_direction")
    assert hasattr(random_record, "sea_level_pressure")
    assert hasattr(random_record, "pressure_tendency")
    assert hasattr(random_record, "air_temperature")
    assert hasattr(random_record, "water_temperature")
    assert hasattr(random_record, "dewpoint_temperature")
    assert hasattr(random_record, "visibility")
    assert hasattr(random_record, "tide")


def test_realtime_wave_summary_data(test_pybuoy: Buoy):
    response = test_pybuoy.realtime.get(station_id=example_station_id, dataset="spec")
    for record in response:
        assert isinstance(record, WaveSummaryObservation)
        assert len(record.__dict__.keys()) == 11

    random_record = response[randrange(len(response.reports))]

    assert (
        hasattr(random_record, "datetime") and type(random_record.datetime) is datetime
    )
    assert hasattr(random_record, "significant_wave_height")
    assert hasattr(random_record, "swell_height")
    assert hasattr(random_record, "swell_period")
    assert hasattr(random_record, "wind_wave_height")
    assert hasattr(random_record, "wind_wave_period")
    assert hasattr(random_record, "swell_direction")
    assert hasattr(random_record, "wind_wave_direction")
    assert hasattr(random_record, "steepness")
    assert hasattr(random_record, "average_wave_period")
    assert hasattr(random_record, "dominant_wave_direction")
