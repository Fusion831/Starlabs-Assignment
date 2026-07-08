from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="The user's full name.")
    email: EmailStr = Field(..., description="The user's email address.")
    password: str = Field(..., min_length=6, max_length=100, description="The user's password (min 6 characters).")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }
