from pybuoy import Buoy

buoy = Buoy(station_id="44065")

meteorological_dataset = "txt"
realtime_meteorological_data = buoy.realtime.get(dataset=meteorological_dataset)

print(f"Station Realtime Data: \n----\n{realtime_meteorological_data}\n----\n")
