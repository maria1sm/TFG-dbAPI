from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    id: str
    email: str
    country: str

class UserResponse(BaseModel):
    id: str
    email: str
    country: str
    register_date: datetime

    class Config:
        orm_mode = True
