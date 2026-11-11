Active Buoys
============

A common use for NDBC's API is to get list of active stations and in order to extract
weather data for analysis.

As always, you need to begin by creating an instance of :class:`.Buoy`:

.. code-block:: python

    import pybuoy

    buoy = pybuoy.Buoy()


.. _get_activestations:

Get List of Active Stations with **pybuoy**
-------------------------------------------

.. code-block:: python

    stations = buoy.stations.get_active()


``stations`` is a list of :class:`.Station`:

.. code-block:: python

    Station(
        id='44065',
        name='New York Harbor Entrance - 15 NM SE of Breezy Point , NY',
        lat=40.368,
        lon=-73.701,
        owner='NDBC',
        program='NDBC Meteorological/Ocean',
        type='buoy',
        elevation=0.0,
        met=True,
        currents=False,
        water_quality=False,
        dart=False,
    )

The flags say which kinds of data NDBC lists for the station, which makes it easy to pick
the stations worth querying:

.. code-block:: python

    for station in stations:
        if station.met:
            observations = buoy.realtime.get(station.id)
