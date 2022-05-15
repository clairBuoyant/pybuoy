from pybuoy import Buoy, Observation


def test_realtime_meterological_data(test_buoypy: Buoy):
    response = test_buoypy.realtime.get()
    for record in response:
        assert isinstance(record[0], Observation)
        assert len(record) == 14  # typically 15, but datetime was abstracted into Observation
