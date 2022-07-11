from pybuoy import Buoy, Observation


def test_realtime_meterological_data(test_pybuoy: Buoy):
    example_station_id = "44065"
    response = test_pybuoy.realtime.get(station_id=example_station_id)
    for record in response:
        assert isinstance(record[0], Observation)
        assert len(record) == 14  # typically 15, but datetime was abstracted into Observation
