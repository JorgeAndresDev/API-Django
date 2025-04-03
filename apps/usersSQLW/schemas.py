from pydantic import BaseModel
from typing import Optional

class UserWSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True  # Para compatibilidad con ORMs

class UserWCreateSchema(BaseModel):
    name: str
    email: str
    password: str

class UserWUpdateSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str