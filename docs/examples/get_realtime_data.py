from pybuoy import Buoy

buoy = Buoy()

example_station_id = "44065"

# dataset="txt" is default
realtime_meteorological_data = buoy.realtime.get(station_id=example_station_id)

print(f"Station Realtime Data: \n----\n{realtime_meteorological_data}\n----\n")
"""Sample Output of realtime_meteorological_data.

The first row of results (i.e., realtime_meteorological_data[0])
returns the following:
[
    Observation(Wind Direction: 190.0 degrees),
    Observation(Wind Speed: 10.0 m/s),
    Observation(Wind Gust: 12.0 m/s),
    Observation(Wave Height: nan m),
    Observation(DOM Wave Period: nan seconds),
    Observation(Average Wave Period: nan seconds),
    Observation(Wave Direction: nan degrees),
    Observation(Sea Pressure: 1012.3 hPa),
    Observation(Air Temperature: nan celcius),
    Observation(Water Temperature: 21.7 celcius),
    Observation(Dewpoint Temperature: nan celcius),
    Observation(Visibility: nan nmi),
    Observation(Pressure Tendency: -0.4 hPa),
    Observation(Tide: nan ft)
]
"""
