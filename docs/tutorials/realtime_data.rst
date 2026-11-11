Realtime Buoy Data
==================

A common use for NDBC's API is to extract weather data and use them
for analysis.

As always, you need to begin by creating an instance of :class:`.Buoy`:

.. code-block:: python

    import pybuoy

    buoy = pybuoy.Buoy()


.. _get_meteorological:

Get Meteorological Data
-----------------------

.. code-block:: python

    observations = buoy.realtime.get("44065", dataset="txt")

.. note::

    ``dataset`` is optional; ``"txt"`` (standard meteorological data) is the default.

``observations`` is a list of :class:`.MeteorologicalObservation` covering the last 45 days,
newest first:

.. code-block:: python

    MeteorologicalObservation(
        time=datetime.datetime(2026, 11, 11, 1, 10, tzinfo=datetime.timezone.utc),
        wind_direction=230.0,
        wind_speed=9.0,
        wind_gust=10.0,
        wave_height=0.7,
        dominant_wave_period=None,
        average_wave_period=3.6,
        wave_direction=109.0,
        sea_level_pressure=1012.6,
        air_temperature=15.6,
        water_temperature=15.8,
        dewpoint_temperature=9.4,
        visibility=None,
        pressure_tendency=None,
        tide=None,
    )

.. note::

    A value the station did not report (``MM`` in NDBC's file) is ``None``.

Values are plain floats, so they can be used directly:

.. code-block:: python

    heights = [o.wave_height for o in observations if o.wave_height is not None]
    print(max(heights))

Units are the ones NDBC publishes. :func:`pybuoy.units` returns them by field name:

.. code-block:: python

    >>> pybuoy.units(pybuoy.MeteorologicalObservation)["wind_speed"]
    'm/s'


.. _get_wave_summary:

Get Wave Summary Data
---------------------

.. code-block:: python

    observations = buoy.realtime.get("44065", dataset="spec")


``observations`` is a list of :class:`.WaveSummaryObservation`:

.. code-block:: python

    WaveSummaryObservation(
        time=datetime.datetime(2026, 11, 11, 1, 10, tzinfo=datetime.timezone.utc),
        significant_wave_height=0.7,
        swell_height=0.3,
        swell_period=10.8,
        wind_wave_height=0.6,
        wind_wave_period=3.6,
        swell_direction='ESE',
        wind_wave_direction='SSW',
        steepness=None,
        average_wave_period=3.6,
        dominant_wave_direction=109.0,
    )

.. note::

    A value NDBC marks ``MM`` or ``N/A`` (here, ``steepness``) is ``None``.


Errors
------

A station id NDBC does not know, or a station that does not publish the dataset, raises
:class:`.StationNotFoundError`:

.. code-block:: python

    try:
        buoy.realtime.get("00000")
    except pybuoy.StationNotFoundError:
        ...
