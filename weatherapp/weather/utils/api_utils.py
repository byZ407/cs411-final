import logging
import os
import requests

from weather.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

OPENWEATHER_URL = os.getenv("OPENWEATHER_URL",
                            "https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}")

def get_weather_data(lat: float, lon: float) -> dict:
    """
    Fetches weather data from OpenWeather API.

    Args:
        lat (float): Latitude coordinate
        lon (float): Longitude coordinate

    Returns:
        dict: Weather data dictionary from OpenWeather API

    Raises:
        ValueError: If the response from OpenWeather is invalid
        RuntimeError: If the request fails due to network issues
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = OPENWEATHER_URL.format(lat=lat, lon=lon, api_key=api_key)

    try:
        logger.info(f"Fetching weather data from OpenWeather API for ({lat}, {lon})")

        response = requests.get(url, timeout=5)

        # Check if the request was successful
        response.raise_for_status()

        weather_data_str = response.text.strip()

        try:
            weather_data = response.json()
        except ValueError:
            logger.error(f"Invalid response from OpenWeather API: {weather_data_str}")
            raise ValueError(f"Invalid response from OpenWeather API: {weather_data_str}")

        logger.debug(f"Received weather data: {weather_data}")
        logger.info(f"Successfully fetched weather data")

        return weather_data

    except requests.exceptions.Timeout:
        logger.error("Request to OpenWeather timed out")
        raise RuntimeError("OpenWeather API request timed out")

    except requests.exceptions.RequestException as e:
        logger.error(f"OpenWeather API request failed: {e}")
        raise RuntimeError(f"OpenWeather API request failed: {e}")

