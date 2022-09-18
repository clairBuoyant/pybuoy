pybuoy - Python NDBC API Wrapper
================================

.. image:: https://img.shields.io/pypi/v/pybuoy?color=blue
    :alt: Latest Version
    :target: https://pypi.python.org/pypi/pybuoy

.. image:: https://img.shields.io/pypi/pyversions/pybuoy
    :alt: Supported Python Versions
    :target: https://pypi.python.org/pypi/pybuoy

.. image:: https://img.shields.io/pypi/dm/pybuoy
    :alt: PyPI - Monthly Downloads
    :target: https://pypi.python.org/pypi/pybuoy


``pybuoy`` is a server-side Python package that was built to facilitate rapid discovery of new data from `NDBC <https://www.ndbc.noaa.gov>`_ with only a single dependency!

Installation
------------

``pybuoy`` is supported on Python 3.10+ and can be installed with either pip or a package manager like `poetry <https://python-poetry.org>`_:

- **with pip**: ``pip install pybuoy``

  - recommended to install any third party library in `python's virtualenv <https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments>`_.

- **with poetry**: ``poetry add pybuoy``

  - automatically creates and manages `python's virtualenvs <https://realpython.com/dependency-management-python-poetry>`_.

Quickstart
----------

.. code-block:: python

    from pybuoy import Buoy

    buoy = Buoy()


With the ``buoy`` instance you can then interact with NDBC:

- `Get all active stations <https://pybuoy.readthedocs.io/en/latest/tutorials/active_buoys.html>`_.

- `Get realtime meteorological data <https://pybuoy.readthedocs.io/en/latest/tutorials/realtime_data.html#get-meteorological-data>`_ for buoy by station_id.

- `Get realtime wave summary data <https://pybuoy.readthedocs.io/en/latest/tutorials/realtime_data.html#get-wave-summary-data>`_ for buoy by station_id.
