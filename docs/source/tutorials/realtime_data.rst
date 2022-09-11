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

    realtime_meteorological_data = buoy.realtime.get(station_id="44065", dataset="txt")

.. note::

    If you are only analyzing Meteorological data, providing **dataset** is optional.

`realtime_meteorological_data` returns an iterable instance of ``MeteorologicalObservations``.

.. code-block:: python

    Observations([
        MeteorologicalObservation(
            datetime=datetime.datetime(2022, 9, 11, 17, 10),
            wind_direction=ObservationDatum(Wind Direction: nan degrees),
            wind_speed=ObservationDatum(Wind Speed: 0.0 m/s),
            wind_gust=ObservationDatum(Wind Gust: 1.0 m/s),
            wave_height=ObservationDatum(Wave Height: nan m),
            dominant_wave_period=ObservationDatum(Dominant Wave Period: nan seconds),
            average_wave_period=ObservationDatum(Average Wave Period: nan seconds),
            wave_direction=ObservationDatum(Wave Direction: nan degrees),
            sea_level_pressure=ObservationDatum(Sea Level Pressure: 1019.5 hPa),
            air_temperature=ObservationDatum(Air Temperature: nan celcius),
            water_temperature=ObservationDatum(Water Temperature: 23.0 celcius),
            dewpoint_temperature=ObservationDatum(Dewpoint Temperature: nan celcius),
            visibility=ObservationDatum(Visibility: nan nmi),
            pressure_tendency=ObservationDatum(Pressure Tendency: nan hPa),
            tide=ObservationDatum(Tide: nan ft)
        ),
        ...
        MeteorologicalObservation(
            datetime=datetime.datetime(2022, 7, 28, 0, 0),
            wind_direction=ObservationDatum(Wind Direction: 190.0 degrees),
            wind_speed=ObservationDatum(Wind Speed: 7.0 m/s),
            wind_gust=ObservationDatum(Wind Gust: 8.0 m/s),
            wave_height=ObservationDatum(Wave Height: nan m),
            dominant_wave_period=ObservationDatum(Dominant Wave Period: nan seconds),
            average_wave_period=ObservationDatum(Average Wave Period: nan seconds),
            wave_direction=ObservationDatum(Wave Direction: nan degrees),
            sea_level_pressure=ObservationDatum(Sea Level Pressure: 1011.1 hPa),
            air_temperature=ObservationDatum(Air Temperature: nan celcius),
            water_temperature=ObservationDatum(Water Temperature: nan celcius),
            dewpoint_temperature=ObservationDatum(Dewpoint Temperature: nan celcius),
            visibility=ObservationDatum(Visibility: nan nmi),
            pressure_tendency=ObservationDatum(Pressure Tendency: -0.8 hP),
            tide=ObservationDatum(Tide: nan ft)
        )
    ])

.. note::

    If no value was recorded (e.g., "Tide: nan ft"), it is set to None.


.. _get_wave_summary:

Get Wave Summary Data
---------------------

.. code-block:: python

    realtimewave_summary_data = buoy.realtime.get(station_id="44065", dataset="spec")


`realtimewave_summary_data` returns an iterable instance of ``WaveSummaryObservations``.

.. code-block:: python

    Observations([
        WaveSummaryObservation(
            datetime=datetime.datetime(2022, 9, 11, 16, 40),
            significant_wave_height=ObservationDatum(Significant Wave Height: 1.1 meters),
            swell_height=ObservationDatum(Swell Height: 1.1 meters),
            swell_period=ObservationDatum(Swell Period: 12.9 seconds),
            wind_wave_height=ObservationDatum(Wind Wave Height: 0.2 meters),
            wind_wave_period=ObservationDatum(Wind Wave Period: 3.1 seconds),
            swell_direction=ObservationDatum(Swell Direction: 'ESE'),
            wind_wave_direction=ObservationDatum(Wind Wave Direction: 'S'),
            steepness=ObservationDatum(Steepness: 'SWELL'),
            average_wave_period=ObservationDatum(Average Wave Period: 8.0 seconds),
            dominant_wave_direction=ObservationDatum(Dominant Wave Direction: 116.0 degrees)
        ),
        ...
        WaveSummaryObservation(
            datetime=datetime.datetime(2022, 7, 28, 0, 40),
            significant_wave_height=ObservationDatum(Significant Wave Height: 0.8 meters),
            swell_height=ObservationDatum(Swell Height: 0.6 meters),
            swell_period=ObservationDatum(Swell Period: 6.2 seconds),
            wind_wave_height=ObservationDatum(Wind Wave Height: 0.6 meters),
            wind_wave_period=ObservationDatum(Wind Wave Period: 3.0 seconds),
            swell_direction=ObservationDatum(Swell Direction: 'SSE'),
            wind_wave_direction=ObservationDatum(Wind Wave Direction: 'S'),
            steepness=ObservationDatum(Steepness: 'AVERAGE'),
            average_wave_period=ObservationDatum(Average Wave Period: 4.2 seconds),
            dominant_wave_direction=ObservationDatum(Dominant Wave Direction: 164.0 degrees)
        ),
    ])

.. note::

    If no value was recorded (e.g., "Steepness: N/A"), it is set to None.
