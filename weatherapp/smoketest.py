import requests

def run_smoketest():
    base_url = "http://localhost:5000/api"
    username = "test"
    password = "test"
    valid_location = {"lat": 42.3493, "lon": -71.1041}
    invalid_location = {"lat": -97.0, "lon": 181.0}

    # Health check
    health_response = requests.get(f"{base_url}/health")
    assert health_response.status_code == 200
    assert health_response.json()["status"] == "success"
    print("Health check successful")

    # Delete user
    delete_user_response = requests.delete(f"{base_url}/reset-users")
    assert delete_user_response.status_code == 200
    assert delete_user_response.json()["status"] == "success"
    print("Reset users successful")

    # Create user
    create_user_response = requests.put(f"{base_url}/create-user", json={
        "username": username,
        "password": password
    })
    assert create_user_response.status_code == 201
    assert create_user_response.json()["status"] == "success"
    print("User creation successful")

    session = requests.Session()

    # Log in
    login_resp = session.post(f"{base_url}/login", json={
        "username": username,
        "password": password
    })
    assert login_resp.status_code == 200
    assert login_resp.json()["status"] == "success"
    print("Login successful")

    # Change password
    change_password_resp = session.post(f"{base_url}/change-password", json={
        "new_password": "new_password"
    })
    assert change_password_resp.status_code == 200
    assert change_password_resp.json()["status"] == "success"
    print("Password change successful")

    # Log in with new password
    login_resp = session.post(f"{base_url}/login", json={
        "username": username,
        "password": "new_password"
    })
    assert login_resp.status_code == 200
    assert login_resp.json()["status"] == "success"
    print("Login with new password successful")

    # Add valid location
    add_loc_resp = session.post(f"{base_url}/add-location", json=valid_location)
    assert add_loc_resp.status_code == 201
    assert "added" in add_loc_resp.json()["message"]
    print("Added valid location successfully")

    # Get weather for valid location
    get_weather1_resp = session.get(f"{base_url}/get-weather/42.3493/-71.1041")
    assert get_weather1_resp.status_code == 200
    assert get_weather1_resp.json()["status"] == "success"
    weather_data = get_weather1_resp.json()["weather"]
    assert "weather" in get_weather_resp.json()
    print("Retrieved weather data for valid location successfully")

    # Try adding duplicate location
    dup_loc_resp = session.post(f"{base_url}/add-location", json=valid_location)
    assert dup_loc_resp.status_code == 400
    assert "already exists" in dup_loc_resp.json()["message"]
    print("Add duplicate location failed as expected")

    # Add invalid location
    invalid_loc_resp = session.post(f"{base_url}/add-location", json=invalid_location)
    assert invalid_loc_resp.status_code == 400
    assert "invalid" in invalid_loc_resp.json()["message"].lower()
    print("Add invalid location failed as expected")

    # Log out
    logout_resp = session.post(f"{base_url}/logout")
    assert logout_resp.status_code == 200
    assert logout_resp.json()["status"] == "success"
    print("Logout successful")

    add_location_logged_out_resp = session.post(f"{base_url}/add-location", json=valid_location)
    # This should fail because we are logged out
    assert add_location_logged_out_resp.status_code == 401
    assert add_location_logged_out_resp.json()["status"] == "error"
    print("Add location after logged out failed as expected")

if __name__ == "__main__":
    run_smoketest()

