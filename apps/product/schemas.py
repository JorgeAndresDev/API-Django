from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    id: str
    nombre: str
    precio: float
    cantidad: int

    class Config:
        from_attributes = True  # Para compatibilidad con ORMs

class ProductCreateSchema(BaseModel):
    nombre: str
    precio: float
    cantidad: int

class ProductUpdateSchema(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    cantidad: Optional[int] = None