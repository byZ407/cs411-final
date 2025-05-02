import pytest

from weather.models.weather_model import WeatherModel

@pytest.fixture()
def weather_model():
    """Fixture to provide a new instance of WeatherModel for each test."""
    return WeatherModel()

@pytest.fixture
def mock_weather_api(mocker):
    mock_response = {
        "lat": BU[0],
        "lon": BU[1],
        "current": {
            "temp": 285.32,
            "weather": [{"description": "clear sky"}]
        }
    }
    mocker.patch("weather.models.weather_model.get_weather_data", return_value=mock_response)
    return mock_response

"""Mock locations"""
BU = (42.3493, -71.1041)
LA = (34.0522, -118.2437)
INV = (-97.3442, 157.6665)

def test_add_location(weather_model, mock_weather_api):
    """Test adding location to the weather_model"""
    weather_model.add_location(BU[0], BU[1])
    assert len(weather_model.locations) == 1

def test_add_location_invalid(weather_model, mock_weather_api):
    """Test adding location that is invalid"""
    with pytest.raises(ValueError, match=r"Latitude -97\.3442.*out of range \(-90 to 90\)"):
        weather_model.add_location(INV[0], BU[1])

def test_add_location_exists(weather_model, mock_weather_api):
    """Test adding existing location to the weather_model"""
    weather_model.add_location(BU[0], BU[1])
    with pytest.raises(ValueError, match=r"Location \(42\.3493.*-71\.1041\) already exists"):
        weather_model.add_location(BU[0], BU[1])

def test_remove_location(weather_model, mock_weather_api):
    """Test removing location to the weather_model"""
    weather_model.add_location(BU[0], BU[1])
    weather_model.remove_location(BU[0], BU[1])
    assert len(weather_model.locations) == 0

def test_remove_location_empty(weather_model, mock_weather_api):
    """Test trying to remove a location from model thats empty"""
    with pytest.raises(ValueError, match="Locations dictionray is empty"):
        weather_model.remove_location(BU[0], BU[1])

def test_get_weather(weather_model, mock_weather_api):
    """Test on getting weather data (dumb)"""
    data = weather_model.get_weather(BU[0], BU[1])
    assert data["lat"] == BU[0] and data["lon"] == BU[1]

def test_get_all_locations(weather_model, mock_weather_api):
    """Test on getting a list of all locations in model"""
    weather_model.add_location(BU[0], BU[1])
    weather_model.add_location(LA[0], LA[1])
    lst = weather_model.get_all_locations()
    assert len(lst) == 2

def test_get_all_locations_empty(weather_model, mock_weather_api):
    """Test on getting a list of all locations on an empty model"""
    with pytest.raises(ValueError, match="Locations dictionray is empty"):
        weather_model.get_all_locations()

def test_update_location(weather_model, mock_weather_api):
    """Test updating a location's weather data"""
    weather_model.add_location(BU[0], BU[1])
    weather_model.update_location(BU[0], BU[1])
    assert (BU[0], BU[1]) in weather_model.locations

def test_update_location_inv(weather_model, mock_weather_api):
    """Test updating a location that does not exist in the list of locations"""
    with pytest.raises(ValueError, match=r"Location \(42\.3493.*-71\.1041\) not found"):
        weather_model.update_location(BU[0], BU[1])
