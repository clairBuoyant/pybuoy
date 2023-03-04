from datetime import datetime, timedelta
from random import randrange

from pybuoy import Buoy
from pybuoy.observation.observation import ForecastObservation


def test_forecast_data(test_pybuoy: Buoy):
    test_begin_date = (datetime.now() + timedelta(1)).isoformat()
    test_end_date = (datetime.now() + timedelta(5)).isoformat()

    response = test_pybuoy.forecasts.get(
        40.369, -73.702531, test_begin_date, test_end_date
    )
    for record in response:
        assert isinstance(record, ForecastObservation)

    random_record = response[randrange(len(response.reports))]
    assert hasattr(random_record, "wind_direction")
    assert hasattr(random_record, "wind_speed")
    assert hasattr(random_record, "wind_gust")
    assert hasattr(random_record, "wave_height")
