class WeatherError(Exception):
    """Base class for weather_mock errors."""


class WeatherNotFound(WeatherError):
    pass


class InvalidGeo(WeatherError):
    pass


class AdminDisabled(WeatherError):
    pass


class UnknownStorm(WeatherError):
    pass


class SinkOutsideWorkspace(WeatherError):
    pass


class CannotRewind(WeatherError):
    pass
