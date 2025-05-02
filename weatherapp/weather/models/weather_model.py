import logging
import os
import time
from typing import Dict

from weather.utils.api_utils import get_weather_data
from weather.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)


class WeatherModel:
    """
    A class to manage weather data for various locations fetched from OpenWeather API.
    """

    def __init__(self):
        """Initializes the WeatherModel with an empty dictionary of locations and caching.

        The TTL (Time To Live) for weather caching is set to a default value from the environment variable "TTL",
        which defaults to 1 hour if not set.
        """
        self.locations: dict[(float, float), dict] = {}
        self._ttl: dict[str, float] = {}
        self.ttl_seconds = int(os.getenv("TTL", 3600))  # Default TTL is 1 hour

    def add_location(self, lat: float, lon: float) -> None:
        """
        Adds a location and its weather data to the model.

        Args:
            lat (float): Latitude of the location.
            lon (float): Longitude of the location.

        Raises:
            ValueError: If the location is invalid or already exists.
        """
        logger.info(f"Received request to add location with coordinates ({lat}, {lon})")
        location = (lat, lon)
        self.validate_location(lat, lon)
        if location in self.locations:
            raise ValueError(f"Location ({lat}, {lon}) already exists")
        weather_data = self.get_weather(lat, lon)
        self.locations[location] = weather_data
        logger.info(f"Successfully added location ({lat}, {lon})")

    def remove_location(self, lat: float, lon: float) -> None:
        """
        Removes an existing location from the model.

        Args:
            lat (float): Latitude of the location.
            lon (float): Longitude of the location.

        Raises:
            ValueError: If the location is not found or model is empty.
        """
        logger.info(f"Received request to remove location with coordinates ({lat}, {lon})")
        self.check_if_empty()
        location = (lat, lon)
        self.validate_location(lat, lon)
        if location not in self.locations:
            raise ValueError(f"Location ({lat}, {lon}) not found")
        del self.locations[location]
        logger.info(f"Successfully removed location ({lat}, {lon})")

    def validate_location(self, lat: float, lon: float) -> None:
        """
        Validates the given latitude and longitude values to ensure they are within valid geographic ranges.

        Args:
            lat (float): Latitude value to validate, must be between -90 and 90.
            lon (float): Longitude value to validate, must be between -180 and 180.

        Raises:
            ValueError: If either latitude or longitude is not a valid number or is out of range.

        """
        try:
            lat, lon = float(lat), float(lon)
            if not (-90 <= lat <= 90):
                raise ValueError(f"Latitude {lat} out of range (-90 to 90)")
            if not (-180 <= lon <= 180):
                raise ValueError(f"Longitude {lon} out of range (-180 to 180)")
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid location: ({lat}, {lon}) - {e}")
            raise ValueError(f"Invalid location: ({lat}, {lon}) - {e}")

    def check_if_empty(self) -> None:
        """
        Checks if the locations dictionary is empty and raises a ValueError if it is.

        Raises:
            ValueError: If the locations dictionary is empty.

        """
        if not self.locations:
            logger.error("Locations dictionary is empty")
            raise ValueError("Locations dictionray is empty")
    
    def get_all_locations(self):
        """ Get a list of the location (float tuples).

        Returns:
            list[(float, float)]: A list of the location coordinates.
        Raises:
            ValueError: If the model is empty.
        """
        logger.info("Received request to get list of all locations")
        self.check_if_empty()
        return [l for l in self.locations.keys()]

    def update_location(self, lat:float, lon:float) -> None:
        """ Update the location in the list with new weather data.

        Args:
            lat (float): The lattitude of the location.
            lon (float): The longitude of the location.

        Raises:
            ValueError: If the location does not exist in the dictionary.
        """
        logger.info("Received request to update location with new data")
        location = (lat, lon)
        if location not in self.locations:
            raise ValueError(f"Location ({lat}, {lon}) not found")
        self.locations[location] = self.get_weather(lat, lon)

    def get_weather(self, lat:float, lon:float):
        """ Get the weather data from a location

        Args:
            lat (float): The location's lattitude
            lon (float): The location's longitude

        Returns:
            dict: A dictionary of all weather data
        """

        return get_weather_data(lat, lon)