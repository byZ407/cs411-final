import pytest
import requests

from weather.utils.api_utils import get_weather_data

LAT = 42.3493
LON = -71.1041
MOCK_RESPONSE = {
    "lat": LAT,
    "lon": LON,
    "current": {
        "temp": 285.32,
        "weather": [{"description": "clear sky"}]
    }
}

@pytest.fixture
def mock_openweather(mocker):
    """Fixture to mock the OpenWeather API response.

    """
    # Patch the requests.get call
    # requests.get returns an object, which we have replaced with a mock object
    mock_response = mocker.Mock()
    # We are giving that object a text attribute
    mock_response.text = str(MOCK_RESPONSE)
    mock_response.json.return_value = MOCK_RESPONSE
    mocker.patch("requests.get", return_value=mock_response)
    return mock_response

def test_get_weather_data(mock_openweather):
    """Test retrieving weather data from the OpenWeather API.

    """
    result = get_weather_data(LAT, LON)

    # Assert that the result matches the mock response
    assert result == MOCK_RESPONSE, f"Expected weather data {MOCK_RESPONSE}, but got {result}"

    # Ensure the correct URL was called
    requests.get.assert_called_once()
    args, kwargs = requests.get.call_args
    assert "lat=42.3493" in args[0]
    assert "lon=-71.1041" in args[0]

def test_get_weather_data_timeout(mocker):
    """Test handling of a timeout when calling the OpenWeather API.

    """
    # Simulate a timeout
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)

    with pytest.raises(RuntimeError, match="OpenWeather API request timed out"):
        get_weather_data(LAT, LON)

def test_get_weather_data_failure(mocker):
    """Test handling of a request failure when calling the OpenWeather API.

    """
    # Simulate a request failure
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("Connection error"))

    with pytest.raises(RuntimeError, match="OpenWeather API request failed: Connection error"):
        get_weather_data(LAT, LON)

def test_get_weather_data_invalid_json(mocker):
    """Test handling of an invalid JSON response from the OpenWeather API.

    """
    # Simulate an invalid response
    mock_response = mocker.Mock()
    mock_response.text = "invalid_json"
    mock_response.json.side_effect = ValueError("No JSON could be decoded")
    mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(ValueError, match="Invalid response from OpenWeather API: invalid_json"):
        get_weather_data(LAT, LON)

