# CS411 Final Project: Weather App
The Weather App allows users to log in and out of their account, save a list of locations that they can get the current weather of, and they can add, remove, and update those locations.

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
  - Code: 400  
    Content: { "error": "Username and password are required" }
  - Code: 500
    Content: { "error": "An internal error occurred while creating user" }
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
Error Response Examples:
  - Code: 400 Content: { "error": "Username and password are required" }
  - Code: 401 Content: { "error": "Invalid username or password" }
  - Code: 500 Content: { "error": "An internal error occurred during login" }
Example Request: { "username": "newuser1", "password": "securepassword" }
Example Response: { "message": "User <username> logged in successfully", "status": "200" }

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
- Example Response: { "message": "Password changed successfully" "status": "200" }

## 
  




