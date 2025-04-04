from datetime import date
from pydantic import BaseModel

class DriverSchema(BaseModel):
    cedula: int;
    nombre_apellido: str;
    cargo: str;
    vencimiento_licencia: date;
    dias_restantes_licencia: int;
    comparendos: str;
    acuerdo_pago: str;
    vencimiento_curso: date;
    dias_restantes_curso: int;

    class Config:
        from_attributes = True  # Para compatibilidad con ORMs

class DriverCreateSchema(BaseModel):
    id_conductor: int | None = None 
    cedula: int;
    nombre_apellido: str;
    cargo: str;
    vencimiento_licencia: date;
    dias_restantes_licencia: int;
    comparendos: str;
    acuerdo_pago: str;
    vencimiento_curso: date;
    dias_restantes_curso: int;

class DriverUpdateSchema(BaseModel):
    id_conductor: int;
    cedula: int;
    nombre_apellido: str;
    cargo: str;
    vencimiento_licencia: date;
    dias_restantes_licencia: int;
    comparendos: str;
    acuerdo_pago: str;
    vencimiento_curso: date;
    dias_restantes_curso: int;