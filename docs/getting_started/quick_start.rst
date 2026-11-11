Quick Start
===========

.. code-block:: python

    from pybuoy import Buoy

    buoy = Buoy()


With the ``buoy`` instance you can then request data from NOAA and NDBC:

- :doc:`Get all active stations </tutorials/active_buoys>`.

- :ref:`Get realtime meteorological data <get_meteorological>` for a buoy by station id.

- :ref:`Get realtime wave summary data <get_wave_summary>` for a buoy by station id.

- :doc:`Get forecast data </tutorials/forecast_data>` for a point by latitude and longitude.

Every result is a list of plain dataclasses (see :doc:`/code_overview/models`):

- times are timezone-aware UTC;
- values are metric, and ``None`` when the source did not report them;
- :func:`pybuoy.units` gives the unit of each field.

Failures raise a subclass of :class:`pybuoy.PybuoyError` (see :doc:`/code_overview/errors`).
