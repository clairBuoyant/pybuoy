"""Print recent observations from NDBC station 44065."""

from pybuoy import Buoy, MeteorologicalObservation, units

buoy = Buoy()

# Standard meteorological data, newest first. dataset="txt" is the default.
observations = buoy.realtime.get("44065")
latest = observations[0]
unit = units(MeteorologicalObservation)

print(f"{latest.time:%Y-%m-%d %H:%M} UTC")
print(f"wind speed  {latest.wind_speed} {unit['wind_speed']}")
print(f"wave height {latest.wave_height} {unit['wave_height']}")

# A value is None when the station did not report it.
heights = [o.wave_height for o in observations if o.wave_height is not None]
print(f"highest waves on record: {max(heights)} {unit['wave_height']}")

# Spectral wave summary.
for wave in buoy.realtime.get("44065", "spec")[:3]:
    print(wave.time, wave.swell_height, wave.swell_period, wave.swell_direction)
