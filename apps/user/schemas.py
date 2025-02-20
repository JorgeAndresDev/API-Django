from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: str
    user: str
    password: str

    class Config:
        from_attributes = True  # Para compatibilidad con ORMs

class UserCreateSchema(BaseModel):
    user: str
    password: str

class UserUpdateSchema(BaseModel):
    user: Optional[str] = None
    password: Optional[str] = None