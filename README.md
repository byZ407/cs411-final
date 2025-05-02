# CS411 Final Project: Weather App
The Weather App allows users to set up their favorite locations and easily view the weather forcasts for these locations. 

# Features
- **Set Favorite Locations:** Users can add their favorite locations to their profile.
- **Get Weather for a Favorite Location:** Provides the current weather details for a user's saved favorite location.
- **View All Favorites with Current Weather:** Displays a list of all favorite locations saved by the user along with the current
weather for each location.
- **See All Favorites:** Allows users to view a simple list of all their saved favorite locations. 
- **Get Historical Weather for a Favorite:** Retrieves historical weather data for a specified favorite location. 
- **Get Forecast for a Favorite:** Offers a detailed weather forecast for a favorite location.

# Routes
## Route: /create-account
- Request Type: POST
- Purpose: Creates a new user account with a username and password.
- Request Body:
  - username (String): The username of the user.
  - password (String): The password to hash and store.
- Response Format: JSON
  - Success Response Example:
    - Code: 200
    - Content: { "message": "User successfully added to the database: <username>" }
- Error Response Examples:
  - Code: 400  
    Content: { "error": "Username and password are required" }
  - Code: 409  
    Content: { "error": "User with username '{username}' already exists" }
  - Code: 500  
    Content: { "error": "Database error: <error_message>" }
- Example Request: { "username": "newuser123", "password": "securepassword" }
- Example Response: { "message": "User successfully added to the database: <username>", "status": "201" }

## Route: /update-password
- Request Type: PUT



