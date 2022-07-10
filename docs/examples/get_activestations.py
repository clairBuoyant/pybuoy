from pybuoy import Buoy

buoy = Buoy()

active_stations = buoy.stations.get_active()

print(f"NDBC Active Stations: \n----\n{active_stations}\n----\n")
