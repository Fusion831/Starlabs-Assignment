from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router

app = FastAPI(
    title="Fitness Studio Booking API",
    description="Backend API for managing user authentication, classes, and bookings.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint to verify the service status.
    """
    return {"status": "ok"}
