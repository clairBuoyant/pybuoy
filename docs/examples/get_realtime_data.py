from pybuoy import Buoy

buoy = Buoy()

example_station_id = "44065"

# dataset="txt" is default
realtime_meteorological_data = buoy.realtime.get(station_id=example_station_id)

print(f"Station Realtime Data: \n----\n{realtime_meteorological_data}\n----\n")
