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

    active_stations = buoy.stations.get_active()


`active_stations` returns an array of station objects.

.. code-block:: python

    [
        {
            'id': '00922',
            'lat': '30',
            'lon': '-90',
            'name': 'OTN201 - 4800922',
            'owner': 'Dalhousie University',
            'pgm': 'IOOS Partners',
            'type': 'other',
            'met': 'n',
            'currents': 'n',
            'waterquality': 'n',
            'dart': 'n'
        },
        ... 1346 more items
    ]
