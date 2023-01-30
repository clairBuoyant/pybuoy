Forecast Data
==================

The new Forecast Data feature that we've implemented uses a different api that is also developed by the NOAA.
The Forecast class still functions just like Realtime just with slight differences.
Differences are:
- Returns a MeteorologicalPredictions object filled with MeteorologicalPrediction objects, instead of returning MeteorologicalObservations object filled with MeteorologicalObservation objects
- MeteorologicalPrediction only has Wind Speed, Wind Gust, Wind Direction, and Wave Height
- The input arguments are Latitude and Longitude coordinates, beginning date which must be no earlier than the current system date, and ending date

As always, you need to begin by creating an instance of :class:`.Buoy`:

.. code-block:: python

    import pybuoy

    buoy = pybuoy.Buoy()

.. _get_forecast:

Get Forecast Data
-----------------------

.. code-block:: python
    # Using Station Id 44065 Coordinates
    from datetime import datetime as dt
    from datetime import timedelta
    begin = dt.today().isoformat()
    end = (dt.today() + timedelta(7)).isoformat()
    forecast_data = buoy.forecasts.get(lat=40.369, lon=-73.703, beginDate=begin, endDate=end)

.. note::
    Input Dates **MUST BE** written in ISO format and passed as a string.

`forecast_data` returns an iterable instance of ``MeteorologicalPredictions``.

.. code-block:: python
    MeteorologicalPredictions(
        _data=[
            MeteorologicalPrediction(
                _datetime=datetime.datetime(2022, 12, 4, 19, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))),
                _wind_direction=ObservationDatum(Wind Direction: 280.0 degrees),
                _wind_speed=ObservationDatum(Wind Speed: 9.0 knots),
                _wind_gust=ObservationDatum(Wind Gust: 11.0 knots),
                _wave_height=ObservationDatum(Wave Height: 2.0 feet)
                ),
            MeteorologicalPrediction(
                _datetime=datetime.datetime(2022, 12, 4, 22, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))),
                _wind_direction=ObservationDatum(Wind Direction: 270.0 degrees),
                _wind_speed=ObservationDatum(Wind Speed: 9.0 knots),
                _wind_gust=ObservationDatum(Wind Gust: 12.0 knots),
                _wave_height=ObservationDatum(Wave Height: 2.0 feet)
                ),
            MeteorologicalPrediction(
                _datetime=datetime.datetime(2022, 12, 5, 1, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))),
                _wind_direction=ObservationDatum(Wind Direction: 270.0 degrees),
                _wind_speed=ObservationDatum(Wind Speed: 9.0 knots),
                _wind_gust=ObservationDatum(Wind Gust: 12.0 knots),
                _wave_height=ObservationDatum(Wave Height: 2.0 feet)
                ),
            ...
                MeteorologicalPrediction(
                    _datetime=datetime.datetime(2022, 12, 11, 7, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))),
                    _wind_direction=ObservationDatum(Wind Direction: 20.0 degrees),
                    _wind_speed=ObservationDatum(Wind Speed: 16.0 knots),
                    _wind_gust=ObservationDatum(Wind Gust: nan knots),
                    _wave_height=ObservationDatum(Wave Height: nan feet)
                ),
                MeteorologicalPrediction(
                    _datetime=datetime.datetime(2022, 12, 11, 13, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))),
                    _wind_direction=ObservationDatum(Wind Direction: 30.0 degrees),
                    _wind_speed=ObservationDatum(Wind Speed: 13.0 knots),
                    _wind_gust=ObservationDatum(Wind Gust: nan knots),
                    _wave_height=ObservationDatum(Wave Height: nan feet)
                ),
                MeteorologicalPrediction(
                    _datetime=datetime.datetime(2022, 12, 11, 19, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))),
                    _wind_direction=ObservationDatum(Wind Direction: 50.0 degrees),
                    _wind_speed=ObservationDatum(Wind Speed: 13.0 knots),
                    _wind_gust=ObservationDatum(Wind Gust: nan knots),
                    _wave_height=ObservationDatum(Wave Height: nan feet))
            ],
        _size=41
    )

.. note::
    If no value was recorded (e.g., “Wave Height: nan ft”), it is set to None.
