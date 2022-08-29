![PyPI - Version](https://img.shields.io/pypi/v/pybuoy?color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybuoy)
![PyPI - Monthly Downloads](https://img.shields.io/pypi/dm/pybuoy)

# pybuoy

`pybuoy` is a server-side Python package that was built to facilitate rapid discovery of new data from [NDBC](https://www.ndbc.noaa.gov/) with only a single dependency!

## Installation

`pybuoy` is supported on Python 3.10+ and can be installed with either `pip` or a package manager like [poetry](https://python-poetry.org):

- **with pip**: `pip install pybuoy`
  - recommended to install any third party library in python's virtualenv. ([ref](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments))
- **with poetry**: `poetry add pybuoy`
  - automatically creates and manages your virtualenvs. ([ref](https://realpython.com/dependency-management-python-poetry))

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

- [Get all active stations](./examples/get_activestations.py).

- [Get realtime meteorological data](./examples/get_realtime_data.py#L12) for buoy by station_id.

- [Get realtime wave summary data](./examples/get_realtime_data.py#L59) for buoy by station_id.
