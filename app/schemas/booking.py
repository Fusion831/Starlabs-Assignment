from datetime import datetime as dt
from pydantic import BaseModel, EmailStr, Field, model_validator

class BookingCreate(BaseModel):
    class_id: int = Field(..., description="The ID of the fitness class to book.")
    client_name: str = Field(..., min_length=1, max_length=100, description="The name of the booking client.")
    client_email: EmailStr = Field(..., description="The email address of the booking client.")

class BookingResponse(BaseModel):
    id: int
    class_id: int
    class_name: str
    datetime: dt
    instructor: str
    client_name: str
    client_email: EmailStr
    booked_at: dt

    model_config = {
        "from_attributes": True
    }

    @model_validator(mode="before")
    @classmethod
    def resolve_fitness_class_fields(cls, data):
        if isinstance(data, dict):
            if "class_name" in data and "datetime" in data and "instructor" in data:
                return data
            
            fitness_class = data.get("fitness_class")
            if fitness_class:
                if isinstance(fitness_class, dict):
                    data["class_name"] = fitness_class.get("name")
                    data["datetime"] = fitness_class.get("datetime")
                    data["instructor"] = fitness_class.get("instructor")
                else:
                    data["class_name"] = getattr(fitness_class, "name", None)
                    data["datetime"] = getattr(fitness_class, "datetime", None)
                    data["instructor"] = getattr(fitness_class, "instructor", None)
            return data

        
        fitness_class = getattr(data, "fitness_class", None)
        if fitness_class:
            return {
                "id": getattr(data, "id", None),
                "class_id": getattr(data, "class_id", None),
                "class_name": getattr(fitness_class, "name", None),
                "datetime": getattr(fitness_class, "datetime", None),
                "instructor": getattr(fitness_class, "instructor", None),
                "client_name": getattr(data, "client_name", None),
                "client_email": getattr(data, "client_email", None),
                "booked_at": getattr(data, "booked_at", None),
            }
        return data
