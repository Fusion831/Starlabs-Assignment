from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_headers(email="class_user@example.com"):
    signup_payload = {
        "name": "Class User",
        "email": email,
        "password": "password123"
    }
    client.post("/signup", json=signup_payload)
    
    login_payload = {
        "email": email,
        "password": "password123"
    }
    response = client.post("/login", json=login_payload)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_class_success():
    headers = get_auth_headers()
    future_time = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    
    payload = {
        "name": "Yoga Flow",
        "datetime": future_time,
        "instructor": "John Doe",
        "available_slots": 15
    }
    response = client.post("/classes", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Yoga Flow"
    assert data["instructor"] == "John Doe"
    assert data["available_slots"] == 15
    assert "id" in data

def test_create_class_unauthorized():
    future_time = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    payload = {
        "name": "Yoga Flow",
        "datetime": future_time,
        "instructor": "John Doe",
        "available_slots": 15
    }
    response = client.post("/classes", json=payload)
    assert response.status_code == 401

def test_create_class_past_datetime():
    headers = get_auth_headers("class_user2@example.com")
    past_time = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    
    payload = {
        "name": "Yoga Flow",
        "datetime": past_time,
        "instructor": "John Doe",
        "available_slots": 15
    }
    response = client.post("/classes", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Class datetime must be in the future"

def test_get_classes_upcoming_and_sorted():
    headers = get_auth_headers("class_user3@example.com")
    
    time_plus_2_days = (datetime.now(timezone.utc) + timedelta(days=2))
    time_plus_1_day = (datetime.now(timezone.utc) + timedelta(days=1))
    
    client.post("/classes", json={
        "name": "HIIT 2",
        "datetime": time_plus_2_days.isoformat(),
        "instructor": "Jane Smith",
        "available_slots": 10
    }, headers=headers)
    
    client.post("/classes", json={
        "name": "Yoga 1",
        "datetime": time_plus_1_day.isoformat(),
        "instructor": "John Doe",
        "available_slots": 20
    }, headers=headers)
    
    response = client.get("/classes")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) >= 2
    
    now = datetime.now(timezone.utc)
    for c in data:
        class_dt = datetime.fromisoformat(c["datetime"])
        if class_dt.tzinfo is None:
            class_dt = class_dt.replace(tzinfo=timezone.utc)
        assert class_dt > now
        
    filtered = [c for c in data if c["name"] in ["HIIT 2", "Yoga 1"]]
    assert len(filtered) == 2
    assert filtered[0]["name"] == "Yoga 1"
    assert filtered[1]["name"] == "HIIT 2"
