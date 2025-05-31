from pydantic import BaseModel, EmailStr
from typing import Optional


class UserProfileSchema(BaseModel):
    password: Optional[str]
    username: str
    firstname: Optional[str]
    email: EmailStr
    phone_number: Optional[str]
    age: Optional[int]

    class Config:
        from_attributes = True

class HouseSchema(BaseModel):
    user_id: int
    total_live_area: int
    built_year: int                      
    garage_cars: int
    basement_area: int
    full_bath: int
    quality_level: int

    class Config:
        from_attributes = True

class HouseListSchema(BaseModel):
    id: int
    user_id: int
    total_live_area: int
    full_bath: int
    quality_level: int
    region: str
    built_year: int
    price: int
    garage_cars: int
    basement_area: int

    class Config:
        from_attributes = True
