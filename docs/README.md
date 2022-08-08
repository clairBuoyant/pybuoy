![PyPI - Version](https://img.shields.io/pypi/v/pybuoy?color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybuoy)
![PyPI - Monthly Downloads](https://img.shields.io/pypi/dm/pybuoy)

# pybuoy

`pybuoy` is a server-side Python package that was built to faciliate rapid discovery of new data from [NDBC](https://www.ndbc.noaa.gov/) with only a single dependency!

## Installation

`pybuoy` is supported on Python 3.10+. The [recommended way to install](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments) `pybuoy` is with `pip` and `virtualenv`.

### Alternative

[Poetry](https://python-poetry.org) is a great alternative for managing your project's dependencies within a `virtualenv` automatically. Adding `pybuoy` is as easy as `poetry add pybuoy` within your project.

For more information on what and how to work with poetry, [click here](https://realpython.com/dependency-management-python-poetry).

## Quickstart

```python
# Demo in python/ipython shell
# Don't forget to install pybuoy first

>>> from pybuoy import Buoy

>>> buoy = Buoy()

>>> buoy
<pybuoy.buoy.Buoy object at 0x10481fc10>
```

## Examples

- [Get all active stations](./docs/examples/get_activestations.py).

- [Get realtime meteorological data](./docs/examples/get_realtime_data.py) for buoy by station_id.
