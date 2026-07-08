from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_headers(email="booking_user@example.com"):
    signup_payload = {
        "name": "Booking User",
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

def create_test_class(headers, name="Yoga", slots=5, days_ahead=1):
    future_time = (datetime.now(timezone.utc) + timedelta(days=days_ahead)).isoformat()
    payload = {
        "name": name,
        "datetime": future_time,
        "instructor": "John Doe",
        "available_slots": slots
    }
    response = client.post("/classes", json=payload, headers=headers)
    return response.json()

def test_book_class_success():
    headers = get_auth_headers()
    fc = create_test_class(headers, name="Pilates", slots=3)
    
    booking_payload = {
        "class_id": fc["id"],
        "client_name": "Booking User",
        "client_email": "booking_user@example.com"
    }
    
    response = client.post("/book", json=booking_payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["class_id"] == fc["id"]
    assert data["class_name"] == "Pilates"
    assert data["instructor"] == "John Doe"
    assert data["client_name"] == "Booking User"
    assert data["client_email"] == "booking_user@example.com"
    assert "+05:30" in data["datetime"]
    assert "+05:30" in data["booked_at"]
    
    classes_resp = client.get("/classes")
    classes_data = classes_resp.json()
    matched_class = next(c for c in classes_data if c["id"] == fc["id"])
    assert matched_class["available_slots"] == 2

def test_book_nonexistent_class():
    headers = get_auth_headers("booking_user2@example.com")
    booking_payload = {
        "class_id": 99999,
        "client_name": "Booking User",
        "client_email": "booking_user2@example.com"
    }
    response = client.post("/book", json=booking_payload, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Fitness class not found"

def test_book_already_started_class(db_session):
    headers = get_auth_headers("booking_user3@example.com")
    
    from app.models.fitness_class import FitnessClass
    
    past_class = FitnessClass(
        name="Past Class",
        datetime=datetime.now(timezone.utc) - timedelta(hours=2),
        instructor="Old Instructor",
        available_slots=10
    )
    db_session.add(past_class)
    db_session.commit()
    db_session.refresh(past_class)
    
    booking_payload = {
        "class_id": past_class.id,
        "client_name": "Booking User",
        "client_email": "booking_user3@example.com"
    }
    response = client.post("/book", json=booking_payload, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Class has already started"

def test_book_no_slots():
    headers = get_auth_headers("booking_user4@example.com")
    fc = create_test_class(headers, name="HIIT Full", slots=1)
    
    booking_payload = {
        "class_id": fc["id"],
        "client_name": "User 1",
        "client_email": "user1@example.com"
    }
    response1 = client.post("/book", json=booking_payload, headers=headers)
    assert response1.status_code == 201
    
    headers2 = get_auth_headers("booking_user5@example.com")
    booking_payload2 = {
        "class_id": fc["id"],
        "client_name": "User 2",
        "client_email": "user2@example.com"
    }
    response2 = client.post("/book", json=booking_payload2, headers=headers2)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "No available slots for this class"

def test_book_duplicate():
    headers = get_auth_headers("booking_user6@example.com")
    fc = create_test_class(headers, name="Zumba Duo", slots=5)
    
    booking_payload = {
        "class_id": fc["id"],
        "client_name": "User",
        "client_email": "booking_user6@example.com"
    }
    response1 = client.post("/book", json=booking_payload, headers=headers)
    assert response1.status_code == 201
    
    response2 = client.post("/book", json=booking_payload, headers=headers)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "You have already booked this class"

def test_get_bookings():
    headers = get_auth_headers("booking_user7@example.com")
    
    # Create classes at different times
    fc_later = create_test_class(headers, name="Later Class", slots=5, days_ahead=3)
    fc_earlier = create_test_class(headers, name="Earlier Class", slots=5, days_ahead=2)
    
    # Book both
    client.post("/book", json={
        "class_id": fc_later["id"],
        "client_name": "User",
        "client_email": "booking_user7@example.com"
    }, headers=headers)
    
    client.post("/book", json={
        "class_id": fc_earlier["id"],
        "client_name": "User",
        "client_email": "booking_user7@example.com"
    }, headers=headers)
    
    # Retrieve bookings
    response = client.get("/bookings", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # They should be sorted by class datetime, so "Earlier Class" first
    assert data[0]["class_name"] == "Earlier Class"
    assert data[1]["class_name"] == "Later Class"
