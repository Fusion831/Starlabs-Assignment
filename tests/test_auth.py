from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup_success():
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/signup", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password_hash" not in data

def test_signup_duplicate_email():
    payload = {
        "name": "Test User 1",
        "email": "dup@example.com",
        "password": "password123"
    }
    response = client.post("/signup", json=payload)
    assert response.status_code == 201

    payload_dup = {
        "name": "Test User 2",
        "email": "dup@example.com",
        "password": "password456"
    }
    response_dup = client.post("/signup", json=payload_dup)
    assert response_dup.status_code == 400
    assert response_dup.json()["detail"] == "Email is already registered"

def test_login_success():
    payload = {
        "name": "Login User",
        "email": "login@example.com",
        "password": "secretpassword"
    }
    client.post("/signup", json=payload)

    login_payload = {
        "email": "login@example.com",
        "password": "secretpassword"
    }
    response = client.post("/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    login_payload = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/login", json=login_payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
