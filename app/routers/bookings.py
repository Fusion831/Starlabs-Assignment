from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.booking import Booking
from app.models.fitness_class import FitnessClass
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse
from app.auth import get_current_user

router = APIRouter(tags=["Bookings"])

@router.post("/book", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def book_class(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fitness_class = db.query(FitnessClass).filter(
        FitnessClass.id == booking_data.class_id
    ).with_for_update().first()

    if not fitness_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitness class not found"
        )

    now = datetime.now(timezone.utc)
    class_dt = fitness_class.datetime
    if class_dt.tzinfo is None:
        class_dt = class_dt.replace(tzinfo=timezone.utc)
    if class_dt <= now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class has already started"
        )

    if fitness_class.available_slots <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No available slots for this class"
        )

    existing_booking = db.query(Booking).filter(
        Booking.class_id == booking_data.class_id,
        Booking.user_id == current_user.id
    ).first()
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already booked this class"
        )

    new_booking = Booking(
        user_id=current_user.id,
        class_id=booking_data.class_id,
        client_name=booking_data.client_name,
        client_email=booking_data.client_email
    )
    fitness_class.available_slots -= 1

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/bookings", response_model=List[BookingResponse])
def get_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookings = db.query(Booking).join(FitnessClass).filter(
        Booking.user_id == current_user.id
    ).order_by(
        FitnessClass.datetime.asc()
    ).all()
    return bookings
