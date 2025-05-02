# CS411 Final Project: Weather App
The Weather App allows users to log in and out of their account, save a list of locations that they can get the current weather of, and add, remove, and update those locations.

# Features
- **Log in and Logout of Their Account**
- **Add and Remove Locations from their List**
- **Get the Weather for Those Locations**

# Routes
## Route: /health
- Request Type: GET
- Purpose: Checks the health
- Response Format: JSON
  - Success Response Example:
  - Code: 200
  - Content: { "status": "healthy" }

## Route: /create-user
- Request Type: PUT
- Purpose: Creates a new user account with a username and password.
- Request Body:
  - username (String): The desired username.
  - password (String): The desired password.
- Response Format: JSON
  - Success Response Example:
    - Code: 201
    - Content: { "message": "User <username> created successfully" }
  - Error Response Examples:
    - Code: 400 Content: { "error": "Username and password are required" }
    - Code: 500 Content: { "error": "An internal error occurred while creating user" }
- Example Request: { "username": "newuser123", "password": "securepassword" }
- Example Response: { "message": "User successfully added to the database: <username>", "status": "200" }

## Route: /login
- Request Type: POST
- Purpose: Authenticate a user and log them in.
- Request Body:
  - username (String): User's chosen username.
  - password (String): User's chosen password.
- Response Format: JSON
  - Success Response Example:
    - Code: 200
    - Content: { "message": "User <username> logged in successfully" }
  - Error Response Examples:
    - Code: 400 Content: { "error": "Username and password are required" }
    - Code: 401 Content: { "error": "Invalid username or password" }
    - Code: 500 Content: { "error": "An internal error occurred during login" }
- Example Request: { "username": "newuser1", "password": "securepassword" }
- Example Response: { "message": "User <username> logged in successfully", "status": "200" }

## Route: /logout
- Request Type: POST
- PURPOSE: Log out the current user.
- Request Body: None
- Response Format: JSON
  - Success Response Example:
    -  Code: 200
    -  Content: { "message": "User logged out successfully" }
- Example Response:{ "message": "User <username> logged out successfully", "status": "200" }

## Route: /change_password
- Request Type: PUT
- Purpose: Allows users to change their password by providing their current password for verification.
- Request Body:
  - new_password (String): The new password to set.
- Response Format: JSON
  - Success Response Example:
    - Code: 200
    - Content: { "message": "Password changed successfully" }
  - Error Response Examples:
    - Code: 400 Content: { "error": "New password is required" }
    - Code: 500 Content: { "error": "An internal error occurred while changing password" }
- Example Request: { "new_password": "newpassword" }
- Example Response: { "message": "Password changed successfully", "status": "200" }

## Route: /reset_users
- Request Type: POST  
- Purpose: Recreates the Users table, deleting all user records.  
- Response Format: JSON  
  - Success Response Example:  
    - Code: 200  
    - Content: { "status": "success", "message": "Users table recreated successfully" }  
  - Error Response Example:  
    - Code: 500
    - Content: { "status": "error", "message": "An internal error occurred while deleting users", "details": "<error_message>" }
- Example Response: { "message": "Users table recreated successfully", "status": 200 }

## Route: /add_location
- Request Type: POST 
- Purpose: Adds a new geographic location (latitude and longitude) to be tracked.  
- Request Body:  
  - lat (Float): Latitude of the location.  
  - lon (Float): Longitude of the location.
- Reponse Format: JSON
  - Success Reponse Example:
    - Code: 200
    - Content: { "status": "success", "message": "Location (37.7749, -122.4194) added successfully" }
  - Error Response Example:
    - Code: 400  Content: { "status": "error", "message": "Latitude and longitude are required" }
    - Code: 500 Content: { "status": "error", "message": "An internal error occurred while adding the location", "details": "<error_message>" }
- Example Request: { "lat": 37.7749, "lon": -122.4194 }
- Example Response {"status": "success", "message": "Location (37.7749, -122.4194) added successfully", "status": 200 }

## Route: /remove_location
- Request Type: DELETE
- Purpose: Removes a location by latitude and longitude.
- Request Body:
  - lat (float): Latitude of the location.
  - lon (float): Longitude of the location.
 - Response Format: JSON
   - Success Response Example:
     - Code: 200
     - Content: { "status": "success", "message": "Location (lat, lon) removed successfully" }
  - Error Resposne Example
    - Code: 400 Content: { "status": "error", "message": "Failed to remove location" }
    - Code: 500 Content: { "status": "error", "message": "An internal error occurred while removing the location", "details": "<error details>" }
  - Example Request: {"lat": 40.7128, "lon": -74.0060 }
  - Example Response: {"status": "success", "message": "Location (40.7128, -74.0060) removed successfully", "status": 200 }
  
## Route: /get_weather
- Request Type: GET
- Purpose: Retrieves current weather data for a specific geographic location.
- Request Body:
  - lat (Float): Latitude of the location.
  - lon (Float): Longitude of the location.
- Response Format: JSON
  - Success Response Example:
    - Code: 200
    - Content: { "status": "success", "message": "Successfully retrieved location weather",  "weather": <data> }
  - Error Response Example:
    - Code: 400: Content { "status": "error", "message": "Failed to get data for location" }
    - Code: 500 Content { "status": "error", "message" There was an error while trying to get data for location" }
- Example Request:  {"lat": 42.3493, "lon": -71.1041 }
- Example Response: {"status":"success", "message": "Successfully retrieved location weather", "weather":<data>, "status": 200 }

## Route: /get_all_locations
- Request Type: GET
- Purpose: Get the list of all locations that have been added.
- Response Format: JSON
  - Success Response Example:
    - Code: 200
    - Content: { "status": "success", "message": "Successfully retrieved list of all locations", "locations": [ [40.7128, -74.0060], [34.0522, -118.2437] ] }
  - Error Response Example:
    - Code: 400
    - Content: { "status": "error", "message": "There was an issue getting list of all locations. }
- Example Response: {"status": "success", "message": "Successfully retrieved list of all locations",
   "locations": [ [40.7128, -74.0060], [34.0522, -118.2437] ], "status": 200 }

## Route: /update_location
- Request Type: PUT
- Purpose: Update a location's weather data.
- Request Body:
  - lat (float): Latitude of the location.
  - lon (float): Longitude of the location.
- Response Format: JSON
  - Success Response Example
    - Code: 200
    - Content: { "status": "success", "message": "Successfully updated location." }
  - Error Response Example
    - Code: 400
    - Content: { "status": "error",  "message": "There was an issue updating location!" }
  - Example Request: {"lat": 40.7128, "lon": -74.0060}
  - Example Response: {  "status": "success", "message": "Successfully updated location.", "status": 200 }
  




