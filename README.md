# Fitness Studio Booking API

## Project Overview
This application provides a backend API for a Fitness Studio Booking system. It allows users to register, log in, view upcoming classes, schedule bookings, and track their bookings.

The API is built using the following technologies:
- **FastAPI**: Modern, high-performance web framework for Python.
- **SQLAlchemy 2.0**: Object-Relational Mapper (ORM) using typed declarative syntax.
- **SQLite**: Lightweight relational database.
- **Pydantic v2**: Data validation and settings management.
- **JWT Authentication**: Token-based secure authentication.

## Setup Instructions

### Prerequisites
- Python 3.12+

### Clone the Repository
```bash
git clone https://github.com/Fusion831/Starlabs-Assignment.git
cd Starlabs-Assignment
```

### Option 1: Setup using standard pip & venv
1. Create and activate a virtual environment:
   - **Windows**:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **Linux/macOS**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Setup using uv
If you have the `uv` package manager installed, simply run:
```bash
uv sync
```
This creates the virtual environment and installs all dependencies in one step.

### Configure the Environment Variables
Copy `.env.example` to `.env`:
- **Windows (PowerShell)**:
  ```powershell
  Copy-Item .env.example .env
  ```
- **Linux/macOS**:
  ```bash
  cp .env.example .env
  ```

Update the values in `.env` as appropriate.

## How to Run Locally

Start the development server:
- **Standard**:
  ```bash
  uvicorn app.main:app --reload
  ```
- **Using uv**:
  ```bash
  uv run uvicorn app.main:app --reload
  ```

Once running, the interactive API docs are available at:
**Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Usage

### 1. User Signup (`POST /signup`)
Registers a new user.
```bash
curl -X POST http://127.0.0.1:8000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "password": "securepassword123"
  }'
```

### 2. User Login (`POST /login`)
Authenticates credentials and returns a JWT access token.
```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "password": "securepassword123"
  }'
```

### 3. Create a Fitness Class (`POST /classes` - Protected)
Creates a new fitness class. Requires a JWT token.
```bash
curl -X POST http://127.0.0.1:8000/classes \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Morning Yoga",
    "datetime": "2026-07-15T08:00:00+05:30",
    "instructor": "John Smith",
    "available_slots": 15
  }'
```

### 4. Get Upcoming Classes (`GET /classes`)
Retrieves all future classes sorted by start time.
```bash
curl -X GET http://127.0.0.1:8000/classes
```

### 5. Book a Fitness Class (`POST /book` - Protected)
Books a slot in a fitness class. Requires a JWT token.
```bash
curl -X POST http://127.0.0.1:8000/book \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "client_name": "Jane Doe",
    "client_email": "jane@example.com"
  }'
```

### 6. View User Bookings (`GET /bookings` - Protected)
Retrieves all bookings for the authenticated user, sorted by class datetime. Requires a JWT token.
```bash
curl -X GET http://127.0.0.1:8000/bookings \
  -H "Authorization: Bearer <your_access_token>"
```

## Running Tests

```bash
# pip
pytest

# uv
uv run pytest
```
