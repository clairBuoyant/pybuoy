"""WIP: Mapping key to unit for Observation."""

# https://www.ndbc.noaa.gov/measdes.shtml

METEOROLOGICAL = {
    # "date_recorded": {"label": "date_recorded", "unit": "datetime"},
    "#YY": {"label": "Year", "unit": "Y"},
    "MM": {"label": "Month", "unit": "m"},
    "DD": {"label": "Day", "unit": "d"},
    "hh": {"label": "Hour", "unit": "H"},
    "mm": {"label": "Minute", "unit": "M"},
    "WDIR": {"label": "Wind Direction", "unit": "degrees"},
    "WSPD": {"label": "Wind Speed", "unit": "m/s"},
    "GST": {"label": "Wind Gust", "unit": "m/s"},
    "WVHT": {"label": "Wave Height", "unit": "m"},
    "DPD": {"label": "DOM Wave Period", "unit": "seconds"},
    "APD": {"label": "Average Wave Period", "unit": "seconds"},
    "MWD": {"label": "Wave Direction", "unit": "degrees"},
    "PRES": {"label": "Sea Pressure", "unit": "hPa"},
    "ATMP": {"label": "Air Temperature", "unit": "celcius"},
    "WTMP": {"label": "Water Temperature", "unit": "celcius"},
    "DEWP": {"label": "Dewpoint Temperature", "unit": "celcius"},
    "VIS": {"label": "Visibility", "unit": "nmi"},  # nautical miles
    "PTDY": {
        "label": "Pressure Tendency",
        "unit": "hPa",
    },  # direction +/- amount of pressure change over 3hr period
    "TIDE": {"label": "Tide", "unit": "ft"},
}

# TODO: update below for dynamic mapping

WAVE_UNITS = {
    "sea_surface_wave_significant_height": "meters",
    "sea_surface_wave_peak_period": "seconds",
    "sea_surface_wave_mean_period": "seconds",
    "sea_surface_swell_wave_significant_height": "meters",
    "sea_surface_swell_wave_period": "seconds",
    "sea_surface_wind_wave_significant_height": "meters",
    "sea_surface_wind_wave_period": "seconds",
    "sea_water_temperature": "celcius",
    "sea_surface_wave_to_direction": "degrees",
    "sea_surface_swell_wave_to_direction": "degrees",
    "sea_surface_wind_wave_to_direction": "degrees",
    "number_of_frequencies": "count",
    "center_frequencies": "Hz",
    "bandwidths": "Hz",
    "spectral_energy": "m**2/Hz",
    "mean_wave_direction": "degrees",
    "principal_wave_direction": "degrees",
    "polar_coordinate_r1": "1",
    "polar_coordinate_r2": "1",
    "calculation_method": None,
    "sampling_rate": "Hz",
}

CURRENT_UNITS = {
    "bin": "count",
    "depth": "meters",
    "direction_of_sea_water_velocity": "degrees",
    "sea_water_speed": "c/s",
    "upward_sea_water_velocity": "c/s",
    "error_velocity": "c/s",
    "platform_orientation": "degrees",
    "platform_pitch_angle": "degrees",
    "platform_roll_angle": "degrees",
    "sea_water_temperature": "celcius",
    "pct_good_3_beam": "percent",
    "pct_good_4_beam": "percent",
    "pct_rejected": "percent",
    "pct_bad": "percent",
    "echo_intensity_beam1": "count",
    "echo_intensity_beam2": "count",
    "echo_intensity_beam3": "count",
    "echo_intensity_beam4": "count",
    "correlation_magnitude_beam1": "count",
    "correlation_magnitude_beam2": "count",
    "correlation_magnitude_beam3": "count",
    "correlation_magnitude_beam4": "count",
    "quality_flags": None,
}

WIND_UNITS = {
    "wind_from_direction": "degrees",
    "wind_speed": "m/s",
    "wind_speed_of_gust": "m/s",
    "upward_air_velocity": "m/s",
}

# REALTIME_WAVE_UNITS = {}

# SPECTRAL_UNITS = {}
