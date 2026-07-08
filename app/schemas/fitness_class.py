from datetime import datetime as dt
from pydantic import BaseModel, Field

class FitnessClassCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="The name of the fitness class.")
    datetime: dt = Field(..., description="The timezone-aware start date and time of the class.")
    instructor: str = Field(..., min_length=1, max_length=100, description="The instructor teaching the class.")
    available_slots: int = Field(..., gt=0, description="The number of available booking slots (must be positive).")

class FitnessClassResponse(BaseModel):
    id: int
    name: str
    datetime: dt
    instructor: str
    available_slots: int

    model_config = {
        "from_attributes": True
    }
