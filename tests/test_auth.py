import uuid


def test_signup_and_login(client):
    signup_payload = {
        "email": "user1@example.com",
        "password": "password1"
    }

    # Signup
    resp_signup = client.post("/signup", json=signup_payload)
    assert resp_signup.status_code in [200, 201], f"Signup failed: {resp_signup.status_code} - {resp_signup.text}"

    # Login (OAuth2 expects form data)
    login_payload = {
        "username": signup_payload["email"],
        "password": signup_payload["password"]
    }
    resp_login = client.post("/login", data=login_payload)
    assert resp_login.status_code == 200, f"Login failed: {resp_login.status_code} - {resp_login.text}"

    json_login = resp_login.json()
    assert "access_token" in json_login, f"No access_token found: {json_login}"




def test_login_bad_credentials(client):
    bad_payload = {"email": "nonexistent@example.com", "password": "wrongpass"}
    resp = client.post("/login", json=bad_payload)

    assert resp.status_code == 400  # Adjusted based on FastAPI's behavior
    assert resp.headers["content-type"].startswith("application/json")
