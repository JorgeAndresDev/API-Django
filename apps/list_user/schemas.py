from pydantic import BaseModel

class UserSchema(BaseModel):
    id: str
    user: str
    password: str
    # Agrega otros campos que tengas en tu base de datos

    class Config:
        from_attributes = True  # Para compatibilidad con ORMs