import logging
from datetime import datetime, timezone, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.fitness_class import FitnessClass
from app.models.user import User
from app.schemas.fitness_class import FitnessClassCreate, FitnessClassResponse
from app.auth import get_current_user

logger = logging.getLogger("app.routers.classes")
router = APIRouter(tags=["Fitness Classes"])

@router.post("/classes", response_model=FitnessClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(
    class_data: FitnessClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(timezone.utc).astimezone(ist_tz)
    class_datetime_ist = class_data.datetime.astimezone(ist_tz)

    if class_datetime_ist <= now_ist:
        logger.warning(f"Class creation failed: datetime {class_datetime_ist} is in the past")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class datetime must be in the future"
        )

    db_class = FitnessClass(
        name=class_data.name,
        datetime=class_datetime_ist,
        instructor=class_data.instructor,
        available_slots=class_data.available_slots
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    logger.info(f"Class created: {db_class.name} (ID: {db_class.id}) by {current_user.email}")
    return db_class

@router.get("/classes", response_model=List[FitnessClassResponse])
def get_classes(db: Session = Depends(get_db)):
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(timezone.utc).astimezone(ist_tz)
    classes = db.query(FitnessClass).filter(
        FitnessClass.datetime > now_ist
    ).order_by(
        FitnessClass.datetime.asc()
    ).all()
    return classes
