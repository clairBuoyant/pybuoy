from datetime import datetime, timedelta

from pybuoy import Buoy


start = datetime.today().isoformat()
end = (datetime.today() + timedelta(7)).isoformat()
buoy = Buoy()

station_44065 = [40.369, -73.703]  # lat, lon

forecast_observations = buoy.forecasts.get(
    lat=station_44065[0], lon=station_44065[1], start_date=start, end_date=end
)

for observation in forecast_observations:
    # IDE should now detect available attributes
    # add code below here
    pass

# Sample Output of Forecast Data
print(f"Station Forecast: {forecast_observations[0]}")
# OUTPUT: Station Forecast: Observation(2022-12-04 19:00:00) # noqa: E501,W505
#
"""forecast_data returns an instance of `ForecastObservations`.
`Observations` is an iterable object and contains a list
of `ForecastObservation`.

Under the hood, the aforementioned sample output provides this object:

    ForecastObservation(
        datetime=datetime.datetime(2022, 12, 4, 19, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))),
        wind_direction=ObservationDatum(Wind Direction: 280.0 degrees),
        wind_speed=ObservationDatum(Wind Speed: 9.0 knots),
        wind_gust=ObservationDatum(Wind Gust: 11.0 knots),
        wave_height=ObservationDatum(Wave Height: 2.0 feet)
    )

`forecast_data[0].wave_height.value` would return 2.0 as type float (defaults to None, if no value was recorded).
"""  # noqa: W505
