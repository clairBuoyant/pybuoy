"""Print the three-day wind and wave forecast for a point."""

from datetime import UTC, datetime, timedelta

from pybuoy import Buoy

buoy = Buoy()

start = datetime.now(UTC)
forecasts = buoy.forecasts.get(
    lat=40.368, lon=-73.701, start=start, end=start + timedelta(days=3)
)

for forecast in forecasts:
    print(
        f"{forecast.time:%a %H:%M} UTC"
        f"  wind {forecast.wind_speed} m/s from {forecast.wind_direction}"
        f"  gust {forecast.wind_gust} m/s"
        f"  waves {forecast.wave_height} m"
    )
