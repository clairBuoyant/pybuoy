=====================================
pybuoy - Python NOAA/NDBC API Wrapper
=====================================

.. image:: https://img.shields.io/pypi/v/pybuoy?color=blue
    :alt: Latest Version
    :target: https://pypi.python.org/pypi/pybuoy

.. image:: https://img.shields.io/pypi/pyversions/pybuoy
    :alt: Supported Python Versions
    :target: https://pypi.python.org/pypi/pybuoy

.. image:: https://img.shields.io/pypi/dm/pybuoy
    :alt: PyPI - Monthly Downloads
    :target: https://pypi.python.org/pypi/pybuoy


``pybuoy`` is a Python wrapper for `NOAA <https://www.noaa.gov>`_ and `NDBC <https://www.ndbc.noaa.gov>`_ REST web services.

Installation
------------

``pybuoy`` is supported on Python 3.12+ and can be installed with pip or a package manager like `uv <https://docs.astral.sh/uv/>`_:

.. code-block:: bash

    pip install pybuoy

.. code-block:: bash

    uv add pybuoy

Quickstart
----------

.. code-block:: python

    from datetime import UTC, datetime, timedelta

    from pybuoy import Buoy

    buoy = Buoy()

    # Realtime observations from a station, newest first.
    latest = buoy.realtime.get("44065")[0]
    print(latest.time, latest.wind_speed, latest.wave_height)

    # Every active station.
    stations = buoy.stations.get_active()

    # Wind and wave forecast for a point.
    now = datetime.now(UTC)
    forecasts = buoy.forecasts.get(40.368, -73.701, now, now + timedelta(days=3))

Results are plain dataclasses. Times are timezone-aware UTC and a value is ``None`` when the
source did not report it. Observations keep the units NDBC publishes and forecasts are in
metres and metres per second; ``pybuoy.units`` gives the unit of every field.

- `Get all active stations <https://pybuoy.readthedocs.io/en/latest/tutorials/active_buoys.html>`_.

- `Get realtime meteorological data <https://pybuoy.readthedocs.io/en/latest/tutorials/realtime_data.html#get-meteorological-data>`_ for buoy by station_id.

- `Get realtime wave summary data <https://pybuoy.readthedocs.io/en/latest/tutorials/realtime_data.html#get-wave-summary-data>`_ for buoy by station_id.

- `Get forecast data <https://pybuoy.readthedocs.io/en/latest/tutorials/forecast_data.html>`_ for buoy by lat/lon.
