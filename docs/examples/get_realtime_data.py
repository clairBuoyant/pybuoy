from pybuoy import Buoy
from pybuoy.observation.observation import (
    MeteorologicalObservation,
    WaveSummaryObservation,
)

buoy = Buoy()

example_station_id = "44065"

# dataset="txt" is default
realtime_meteorological_data = buoy.realtime.get(station_id=example_station_id)

for record in realtime_meteorological_data:
    # add to support your editor's intellisense with this check
    is_meteorological = isinstance(record, MeteorologicalObservation)
    if not is_meteorological:
        break
    # IDE will now detect available attributes
    # when interacting with the iterator variable (record)

    # add code below here

# Sample Output of Meteorological Data
print(f"Station Realtime Data (latest record): {realtime_meteorological_data[0]}")
# OUTPUT: Station Realtime Data (latest record): Observation(2022-08-28 21:10:00) # noqa: E501,W505
#
"""realtime_meteorological_data returns an instance of `Observations`.
`Observations` is an iterable object and contains a list
of `MeteorologicalObservation`.

Under the hood, the aforementioned sample output provides this object:

    MeteorologicalObservation(
        datetime=datetime.datetime(2022, 8, 28, 16, 20),
        wind_direction=ObservationDatum(Wind Direction: 80.0 degrees),
        wind_speed=ObservationDatum(Wind Speed: 8.0 m/s),
        wind_gust=ObservationDatum(Wind Gust: 10.0 m/s),
        wave_height=ObservationDatum(Wave Height: nan m),
        dominant_wave_period=ObservationDatum(Dominant Wave Period: nan seconds),
        average_wave_period=ObservationDatum(Average Wave Period: nan seconds),
        wave_direction=ObservationDatum(Wave Direction: nan degrees),
        sea_level_pressure=ObservationDatum(Sea Level Pressure: 1020.9 hPa),
        air_temperature=ObservationDatum(Air Temperature: nan celcius),
        water_temperature=ObservationDatum(Water Temperature: 23.9 celcius),
        dewpoint_temperature=ObservationDatum(Dewpoint Temperature: nan celcius),
        visibility=ObservationDatum(Visibility: nan nmi),
        pressure_tendency=ObservationDatum(Pressure Tendency: nan hPa),
        tide=ObservationDatum(Tide: nan ft)
    )

`realtime_meteorological_data[0].sea_level_pressure.value` would return
1020.9 as type float (defaults to None, if no value was recorded).
"""  # noqa: W505


wave_summary = "spec"

realtime_wave_summary_data = buoy.realtime.get(
    station_id=example_station_id, dataset=wave_summary
)

for record in realtime_wave_summary_data:
    # add to support your editor's intellisense with this check
    is_wave_summary = isinstance(record, WaveSummaryObservation)
    if not is_wave_summary:
        break
    # IDE will now detect available attributes
    # when interacting with the iterator variable (record)
    # add code below here


# Sample Output of Wave Summary Data
print(f"Station Realtime Data (latest record): {realtime_wave_summary_data[0]}")
# OUTPUT: Station Realtime Data (latest record): Observation(2022-08-28 20:40:00) # noqa: E501,W505
#
"""realtime_wave_summary_data returns an instance of `Observations`.
`Observations` is an iterable object and contains a list
of `WaveSummaryObservation`.

Under the hood, the aforementioned sample output provides this object:

    WaveSummaryObservation(
        datetime=datetime.datetime(2022, 8, 28, 20, 40),
        significant_wave_height=ObservationDatum(Significant Wave Height: 0.9 meters),
        swell_height=ObservationDatum(Swell Height: 0.4 meters),
        swell_period=ObservationDatum(Swell Period: 7.1 seconds),
        wind_wave_height=ObservationDatum(Wind Wave Height: 0.8 meters),
        wind_wave_period=ObservationDatum(Wind Wave Period: 5.0 seconds),
        swell_direction=ObservationDatum(Swell Direction: SE),
        wind_wave_direction=ObservationDatum(Wind Wave Direction: E),
        steepness=ObservationDatum(Steepness: VERY_STEEP),
        average_wave_period=ObservationDatum(Average Wave Period: 4.1 seconds),
        dominant_wave_direction=ObservationDatum(Dominant Wave Direction: 97.0 degrees)
    )

`realtime_wave_summary_data[0].average_wave_period.value` would return
4.1 as type float (defaults to None, if no value was recorded).
"""  # noqa: W505
