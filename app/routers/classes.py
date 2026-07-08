from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.fitness_class import FitnessClass
from app.models.user import User
from app.schemas.fitness_class import FitnessClassCreate, FitnessClassResponse
from app.auth import get_current_user

router = APIRouter(tags=["Fitness Classes"])

@router.post("/classes", response_model=FitnessClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(
    class_data: FitnessClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    now = datetime.now(timezone.utc)
    if class_data.datetime <= now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class datetime must be in the future"
        )
    
    db_class = FitnessClass(
        name=class_data.name,
        datetime=class_data.datetime,
        instructor=class_data.instructor,
        available_slots=class_data.available_slots
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

@router.get("/classes", response_model=List[FitnessClassResponse])
def get_classes(db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    classes = db.query(FitnessClass).filter(
        FitnessClass.datetime > now
    ).order_by(
        FitnessClass.datetime.asc()
    ).all()
    return classes
