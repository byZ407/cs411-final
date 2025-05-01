import pytest

from weather.models.weather_model import WeatherModel


@pytest.fixture()
def weather_model():
    """Fixture to provide a new instance of WeatherModel for each test."""
    return WeatherwModel()


