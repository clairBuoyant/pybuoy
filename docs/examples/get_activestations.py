from pybuoy import Buoy

buoy = Buoy(station_id="44065")

active_stations = buoy.stations.get_active()

print(f"NDBC Active Stations: \n----\n{active_stations}\n----\n")
