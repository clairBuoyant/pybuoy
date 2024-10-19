Forecast
========

Forecast information is provided by NOAA's `National Digital Forecast Database <https://www.ncei.noaa.gov/products/weather-climate-models/national-digital-forecast-database>`_.

As always, you need to begin by creating an instance of :class:`.Buoy`:

.. code-block:: python

    from pybuoy import Buoy

    buoy = Buoy()

.. _get_forecast:

Get Forecast Data
-----------------

.. code-block:: python

    from datetime import datetime, timedelta

    start = datetime.today().isoformat()
    end = (datetime.today() + timedelta(7)).isoformat()

    station_44065 = [40.368, -73.701] # lat, lon

    forecast_data = buoy.forecasts.get(
        lat=station_44065[0],
        lon=station_44065[1],
        start_date=start,
        end_date=end
    )

.. note::

    start_date and end_date **MUST BE** a valid ISO Date string.

`forecast_data` returns an iterable instance of ``ForecastObservations``.

.. code-block:: python

    ForecastObservations(
        reports=[
            ForecastObservation(
                datetime=datetime.datetime(2022, 12, 4, 19, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))),
                wind_direction=ObservationDatum(Wind Direction: 280.0 degrees),
                wind_speed=ObservationDatum(Wind Speed: 9.0 knots),
                wind_gust=ObservationDatum(Wind Gust: 11.0 knots),
                wave_height=ObservationDatum(Wave Height: 2.0 feet)
            ),
            ForecastObservation(
                datetime=datetime.datetime(2022, 12, 4, 22, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))),
                wind_direction=ObservationDatum(Wind Direction: 270.0 degrees),
                wind_speed=ObservationDatum(Wind Speed: 9.0 knots),
                wind_gust=ObservationDatum(Wind Gust: 12.0 knots),
                wave_height=ObservationDatum(Wave Height: 2.0 feet)
            ),
            ForecastObservation(
                datetime=datetime.datetime(2022, 12, 5, 1, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))),
                wind_direction=ObservationDatum(Wind Direction: 270.0 degrees),
                wind_speed=ObservationDatum(Wind Speed: 9.0 knots),
                wind_gust=ObservationDatum(Wind Gust: 12.0 knots),
                wave_height=ObservationDatum(Wave Height: 2.0 feet)
            ),
            ...
            ForecastObservation(
                datetime=datetime.datetime(2022, 12, 11, 7, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))),
                wind_direction=ObservationDatum(Wind Direction: 20.0 degrees),
                wind_speed=ObservationDatum(Wind Speed: 16.0 knots),
                wind_gust=ObservationDatum(Wind Gust: nan knots),
                wave_height=ObservationDatum(Wave Height: nan feet)
            ),
            ForecastObservation(
                datetime=datetime.datetime(2022, 12, 11, 13, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))),
                wind_direction=ObservationDatum(Wind Direction: 30.0 degrees),
                wind_speed=ObservationDatum(Wind Speed: 13.0 knots),
                wind_gust=ObservationDatum(Wind Gust: nan knots),
                wave_height=ObservationDatum(Wave Height: nan feet)
            ),
            ForecastObservation(
                datetime=datetime.datetime(2022, 12, 11, 19, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))),
                wind_direction=ObservationDatum(Wind Direction: 50.0 degrees),
                wind_speed=ObservationDatum(Wind Speed: 13.0 knots),
                wind_gust=ObservationDatum(Wind Gust: nan knots),
                wave_height=ObservationDatum(Wave Height: nan feet)
            )
        ],
        size=41
    )

.. note::

    If no value was recorded (e.g., “Wave Height: nan ft”), it is set to None.
