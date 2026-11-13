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

    from datetime import UTC, datetime, timedelta

    start = datetime.now(UTC)
    end = start + timedelta(days=3)

    forecasts = buoy.forecasts.get(lat=40.368, lon=-73.701, start=start, end=end)

.. note::

    ``start`` and ``end`` **must be** timezone-aware; a naive datetime raises ``ValueError``.
    Only forecasts between the two instants are returned.

``forecasts`` is a list of :class:`.Forecast`, oldest first:

.. code-block:: python

    Forecast(
        time=datetime.datetime(2026, 11, 11, 5, 0, tzinfo=datetime.timezone.utc),
        wind_direction=290.0,
        wind_speed=6.69,
        wind_gust=9.77,
        wave_height=0.91,
    )

Values are metric (``m/s`` and ``m``). NOAA publishes whole knots and whole feet, which pybuoy
converts, so wind speed moves in steps of about 0.5 m/s and wave height in steps of about 0.3 m.

.. note::

    A value NOAA does not forecast for a given time is ``None``. Wave height, for example,
    is forecast over a shorter period than wind.

A point outside the area NOAA forecasts for returns an empty list.
