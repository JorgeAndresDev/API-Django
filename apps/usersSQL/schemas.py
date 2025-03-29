from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: str
    name_surname: str
    email_user: str
    pass_user: str

    class Config:
        from_attributes = True  # Para compatibilidad con ORMs

class UserCreateSchema(BaseModel):
    name_surname: str
    email_user: str
    pass_user: str

class UserUpdateSchema(BaseModel):
    id: str
    name_surname: Optional[str] = None
    email_user: Optional[str] = None
    pass_user: Optional[str] = None