from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from config import ProductionConfig

from weather.db import db
from weather.models.weather_model import WeatherModel
from weather.models.user_model import Users
from weather.utils.logger import configure_logger

load_dotenv()

def create_app(config_class=ProductionConfig) -> Flask:
    """Create a Flask application with the specified configuration.

    Args:
        config_class (Config): The configuration class to use.

    Returns:
        Flask app: The configured Flask application.

    """
    app = Flask(__name__)
    configure_logger(app.logger)

    app.config.from_object(config_class)

    # Initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.filter_by(username=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        return make_response(jsonify({
            "status": "error",
            "message": "Authentication required"
        }), 401)

    weather_model = WeatherModel()

    #####################################################
    #
    # Healthcheck
    #
    #####################################################

    @app.route('/api/health', methods=['GET'])
    def healthcheck() -> Response:
        """Health check route to verify the service is running.

        Returns:
            JSON response indicating the health status of the service.

        """
        app.logger.info("Health check endpoint hit")
        return make_response(jsonify({
            'status': 'success',
            'message': 'Service is running'
        }), 200)

    ##########################################################
    #
    # User Management
    #
    ##########################################################

    @app.route('/api/create-user', methods=['PUT'])
    def create_user() -> Response:
        """Register a new user account.

        Expected JSON Input:
            - username (str): The desired username.
            - password (str): The desired password.

        Returns:
            JSON response indicating the success of the user creation.

        Raises:
            400 error if the username or password is missing.
            500 error if there is an issue creating the user in the database.
        """
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Username and password are required"
                }), 400)

            Users.create_user(username, password)
            return make_response(jsonify({
                "status": "success",
                "message": f"User '{username}' created successfully"
            }), 201)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"User creation failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while creating user",
                "details": str(e)
            }), 500)

    @app.route('/api/login', methods=['POST'])
    def login() -> Response:
        """Authenticate a user and log them in.

        Expected JSON Input:
            - username (str): The username of the user.
            - password (str): The password of the user.

        Returns:
            JSON response indicating the success of the login attempt.

        Raises:
            401 error if the username or password is incorrect.
        """
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Username and password are required"
                }), 400)

            if Users.check_password(username, password):
                user = Users.query.filter_by(username=username).first()
                login_user(user)
                return make_response(jsonify({
                    "status": "success",
                    "message": f"User '{username}' logged in successfully"
                }), 200)
            else:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid username or password"
                }), 401)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 401)
        except Exception as e:
            app.logger.error(f"Login failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred during login",
                "details": str(e)
            }), 500)

    @app.route('/api/logout', methods=['POST'])
    @login_required
    def logout() -> Response:
        """Log out the current user.

        Returns:
            JSON response indicating the success of the logout operation.

        """
        logout_user()
        return make_response(jsonify({
            "status": "success",
            "message": "User logged out successfully"
        }), 200)

    @app.route('/api/change-password', methods=['POST'])
    @login_required
    def change_password() -> Response:
        """Change the password for the current user.

        Expected JSON Input:
            - new_password (str): The new password to set.

        Returns:
            JSON response indicating the success of the password change.

        Raises:
            400 error if the new password is not provided.
            500 error if there is an issue updating the password in the database.
        """
        try:
            data = request.get_json()
            new_password = data.get("new_password")

            if not new_password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "New password is required"
                }), 400)

            username = current_user.username
            Users.update_password(username, new_password)
            return make_response(jsonify({
                "status": "success",
                "message": "Password changed successfully"
            }), 200)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Password change failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while changing password",
                "details": str(e)
            }), 500)

    @app.route('/api/reset-users', methods=['DELETE'])
    def reset_users() -> Response:
        """Recreate the users table to delete all users.

        Returns:
            JSON response indicating the success of recreating the Users table.

        Raises:
            500 error if there is an issue recreating the Users table.
        """
        try:
            app.logger.info("Received request to recreate Users table")
            with app.app_context():
                Users.__table__.drop(db.engine)
                Users.__table__.create(db.engine)
            app.logger.info("Users table recreated successfully")
            return make_response(jsonify({
                "status": "success",
                "message": f"Users table recreated successfully"
            }), 200)

        except Exception as e:
            app.logger.error(f"Users table recreation failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while deleting users",
                "details": str(e)
            }), 500)

    ##########################################################
    #
    # Weather Management
    #
    ##########################################################

    @app.route('/weather/locations', methods=['POST'])
    @login_required
    def add_location() -> Response:
        """Add a new location to track.

        Expected JSON Input:
            - lat (float): Latitude of the location.
            - lon (float): Longitude of the location.

        Returns:
            JSON response indicating success of the addition.

        Raises:
            400 error if input validation fails.
            500 error if there is an issue adding the location.
        """
        try:
            app.logger.info("Received request to add new location")

            data = request.get_json()
            
            if not data or 'lat' not in data or 'lon' not in data:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Latitude and longitude are required"
                }), 400)

            lat = data.get("lat")
            lon = data.get("lon")

            app.logger.info(f"Adding location ({lat}, {lon})")
            weather_model.add_location(lat, lon)

            app.logger.info(f"Successfully added location ({lat}, {lon})")
            return make_response(jsonify({
                "status": "success",
                "message": f"Location ({lat}, {lon}) added successfully"
            }), 201)

        except ValueError as e:
            app.logger.warning(f"Failed to add location: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)

        except Exception as e:
            app.logger.error(f"Failed to add location: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while adding the location",
                "details": str(e)
            }), 500)

    @app.route('/weather/locations/<lat>/<lon>', methods=['DELETE'])
    @login_required
    def remove_location(lat: float, lon: float) -> Response:
        """Remove a location by latitude and longitude.

        Path Parameters:
            - lat (float): Latitude of the location.
            - lon (float): Longitude of the location.

        Returns:
            JSON response indicating success of the removal.

        Raises:
            400 error if the location does not exist
            500 error if there is an issue removing the location.
        """
        try:
            app.logger.info(f"Received request to remove location ({lat}, {lon})")

            weather_model.remove_location(lat, lon)
            app.logger.info(f"Successfully removed location ({lat}, {lon})")
            return make_response(jsonify({
                "status": "success",
                "message": f"Location ({lat}, {lon}) removed successfully"
            }), 200)

        except ValueError as e:
            app.logger.warning(f"Failed to remove location: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Failed to remove location: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while removing the location",
                "details": str(e)
            }), 500)

    @app.route('/weather/<lat>/<lon>', methods=['GET'])
    @login_required
    def get_weather(lat:float, lon:float) -> Response:
        """Get a location's weather data.

        Path Parameters:
            - lat (float): Latitude of the location.
            - lon (float): Longitude of the location.

        Returns:
            JSON containing the weather data.

        Raises:
            400 error if api return invalid response.
            500 error if there is a runtime error.
        """
        try:
            app.logger.info(f"Trying to retrieve weather data for ({lat}, {lon})")
            data = weather_model.get_weather(lat, lon)
            app.logger.info(f"Retrieved data for ({lat}, {lon})!")

            return make_response(jsonify({
                "status": "success",
                "message": "Successfully retrieved location weather",
                "weather": data,
            }), 200)
        except ValueError as e:
            app.logger.warning(f"Failed to get data for location: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except RuntimeError as e:
            app.logger.error(f"There was an error while trying to get data for location: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 500)

    
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.logger.info("Starting Flask app...")
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        app.logger.error(f"Flask app encountered an error: {e}")
    finally:
        app.logger.info("Flask app has stopped.")

