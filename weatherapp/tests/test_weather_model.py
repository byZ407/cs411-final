import pytest

from weather.models.weather_model import WeatherModel


@pytest.fixture()
def weather_model():
    """Fixture to provide a new instance of WeatherModel for each test."""
    return WeatherModel()

"""Mock locations"""
BU = (42.3493, -71.1041)
INV = (-97.3442, 157.6665)

def test_add_location(weather_model, mocker):
    """Test adding location to the weather_model"""
    weather_model.add_location(BU[0], BU[1])
    assert len(weather_model.locations) == 1

def test_add_location_invalid(weather_model, mocker):
    """Test adding location that is invalid"""
    with pytest.raises(ValueError, match="Latitude -97.3442 out of range (-90 to 90)"):
        weather_model.add_location(INV[0], INV[1])

def test_add_location_exists(weather_model, mocker):
    """Test adding existing location to the weather_model"""
    weather_model.add_location(BU[0], BU[1])
    with pytest.raises(ValueError, match="Location (42.3493, -71.1041) already exists"):
        weather_model.add_location(BU[0], BU[1])

def test_remove_location(weather_model, mocker):
    """Test removing location to the weather_model"""
    weather_model.add_location(BU[0], BU[1])
    weather_model.remove_location(BU[0], BU[1])
    assert len(weather_model.locations) == 0

def test_remove_location_empty(weather_model, mocker):
    """Test trying to remove a location from model thats empty"""
    with pytest.raises(ValueError, match="Locations dictionray is empty"):
        weather_model.remove_location(BU[0], BU[1])

def test_get_weather(weather_model, mocker):
    """Test on getting weather data (dumb)"""
    data = weather_model.get_weather(BU[0], BU[1])
    assert data["lat"] == BU[0] and data["lon"] == BU[0]