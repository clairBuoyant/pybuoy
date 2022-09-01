# TODO: incorporate to improve performance
class MeteorologicalMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs["__slots__"] = (
            "wind_direction",
            "wind_speed",
            "wind_gust",
            "wave_height",
            "dominant_wave_period",
            "average_wave_period",
            "wave_direction",
            "sea_level_pressure",
            "air_temperature",
            "water_temperature",
            "dewpoint_temperature",
            "visibility",
            "pressure_tendency",
            "tide",
            "_datetime",
        )
        return super(MeteorologicalMeta, cls).__new__(cls, name, bases, attrs)


class WaveMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs["__slots__"] = (
            "sea_surface_wave_significant_height",
            "sea_surface_wave_peak_period",
            "sea_surface_wave_mean_period",
            "sea_surface_swell_wave_significant_height",
            "sea_surface_swell_wave_period",
            "sea_surface_wind_wave_significant_height",
            "sea_surface_wind_wave_period",
            "sea_water_temperature",
            "sea_surface_wave_to_direction",
            "sea_surface_swell_wave_to_direction",
            "sea_surface_wind_wave_to_direction",
            "number_of_frequencies",
            "center_frequencies",
            "bandwidths",
            "spectral_energy",
            "mean_wave_direction",
            "principal_wave_direction",
            "polar_coordinate_r1",
            "polar_coordinate_r2",
            "calculation_method",
            "sampling_rate",
            "_datetime",
        )
        return super(WaveMeta, cls).__new__(cls, name, bases, attrs)
