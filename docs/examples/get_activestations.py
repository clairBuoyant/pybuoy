"""List the active NDBC stations that report meteorological data."""

from pybuoy import Buoy

stations = Buoy().stations.get_active()
print(f"{len(stations)} active stations")

for station in stations:
    if station.met:
        print(station.id, station.name, station.lat, station.lon)
