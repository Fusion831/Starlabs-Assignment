# Fitness Studio Booking API

A production-style, modular backend API built using **FastAPI** and **SQLAlchemy** for a fictional fitness studio. The application supports user authentication, class creation, and slot booking with capacity validation and automatic timezone handling.

---

## 🛠️ Tech Stack

- **Runtime:** Python 3.12+
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous Web Framework)
- **Database:** SQLite (SQLAlchemy ORM)
- **Package & Environment Manager:** [uv](https://github.com/astral-sh/uv) (Fast, modern Python package manager)
- **Testing:** pytest & HTTPX (for API integration testing)

---

## 📁 Project Structure

```text
├── app/
│   ├── models/          # SQLAlchemy database models
│   │   └── __init__.py
│   ├── schemas/         # Pydantic schemas (Request/Response models)
│   │   └── __init__.py
│   ├── routers/         # API endpoint routers
│   │   └── __init__.py
│   ├── auth.py          # Authentication utilities (JWT, password hashing)
│   ├── database.py      # SQLAlchemy engine, session, and declarative base
│   ├── dependencies.py  # Shared dependencies (e.g., get_db)
│   └── main.py          # FastAPI application entry point
├── tests/               # Test suite
│   ├── __init__.py
│   └── test_main.py     # Main application integration tests
├── .env.example         # Environment variables template
├── .gitignore           # Ignored files for Git
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation (this file)
```

---

## 🚀 Getting Started

This project uses `uv` for managing dependencies and virtual environments.

### Prerequisites

- Python 3.12+ installed.
- `uv` installed. If you do not have `uv`, install it via:
  ```bash
  # On macOS/Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # On Windows (PowerShell)
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd StarLabs
   ```

2. **Initialize a virtual environment using Python 3.12:**
   ```bash
   uv venv --python 3.12
   ```

3. **Activate the virtual environment:**
   - **Windows (CMD/PowerShell):**
     ```powershell
     .venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install the dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

5. **Configure Environment Variables:**
   Copy the template file to create a local `.env` configuration:
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and customize the configuration if needed.

---

## ⚙️ Running the Application

To run the development server locally:

```bash
uv run uvicorn app.main:app --reload
```

The application will start, and you can access:
- **Interactive Documentation (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative Documentation (Redoc):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Running Tests

Verify the project setup and endpoint functionality:

```bash
uv run pytest
```

---

## 📖 API Usage & Examples

### 1. System Health Check
Verify the service is up and running.

- **Endpoint:** `GET /health`
- **Authentication:** None
- **Sample Request:**
  ```bash
  curl -X GET http://127.0.0.1:8000/health
  ```
- **Sample Response:**
  ```json
  {
    "status": "ok"
  }
  ```

---

## 🗓️ Future Endpoint Specifications (For Reference)

The following endpoints will be implemented in subsequent phases:

### User Management
- `POST /signup`: Register a new user.
- `POST /login`: Authenticate credentials and retrieve access tokens.

### Class Management (Authenticated Users)
- `POST /classes`: Create a new fitness class.
- `GET /classes`: Fetch all upcoming fitness classes (IST timezone).

### Booking Management (Authenticated Users)
- `POST /book`: Book a slot in a class (validated against capacity).
- `GET /bookings`: Fetch booking history for the current authenticated user.
