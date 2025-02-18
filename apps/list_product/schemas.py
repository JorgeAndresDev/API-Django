from pydantic import BaseModel

class ProductSchema(BaseModel):
    id: str
    nombre: str
    precio: float
    cantidad: int

    class Config:
        from_attributes = True  # Para compatibilidad con ORMs