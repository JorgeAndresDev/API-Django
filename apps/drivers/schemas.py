from pydantic import BaseModel
from typing import Optional

class DriverSchema(BaseModel):
    cedula: int;
    nombre_apellido: str;
    cargo: str;
    vencimiento_licencia: str;
    dias_restantes_licencia: int;
    comparendos: str;
    acuerdo_pago: str;
    vencimiento_curso: str;
    dias_restantes_curso: int;

    class Config:
        from_attributes = True  # Para compatibilidad con ORMs

class DriverCreateSchema(BaseModel):
    cedula: int;
    nombre_apellido: str;
    cargo: str;
    vencimiento_licencia: str;
    dias_restantes_licencia: int;
    comparendos: str;
    acuerdo_pago: str;
    vencimiento_curso: str;
    dias_restantes_curso: int;

class DriverUpdateSchema(BaseModel):
    cedula: int;
    nombre_apellido: str;
    cargo: str;
    vencimiento_licencia: str;
    dias_restantes_licencia: int;
    comparendos: str;
    acuerdo_pago: str;
    vencimiento_curso: str;
    dias_restantes_curso: int;