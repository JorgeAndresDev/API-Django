from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True  # Para compatibilidad con ORMs

class UserCreateSchema(BaseModel):
    name: str
    email: str
    password: str

class UserUpdateSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str