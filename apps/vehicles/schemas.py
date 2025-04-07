from datetime import date
from pydantic import BaseModel

class VehiclesSchema(BaseModel):
    ubicacion: str;
    placa: str;
    numero_motor: str;
    color_cabina: str;
    marca: str;
    linea: str;
    modelo: str;
    vencimiento_soat: date;
    dias_vigentes_soat: int;
    vencimiento_rtm: date;
    dias_vigentes_rtm: int;
    vencimiento_permiso: date;
    dias_vigentes_permiso: int;
    vencimiento_extintor: date;
    dias_vigentes_extintor: int;

class VehiclesCreateSchema(BaseModel):
    id: int;
    ubicacion: str;
    placa: str;
    numero_motor: str;
    color_cabina: str;
    marca: str;
    linea: str;
    modelo: str;
    vencimiento_soat: date;
    dias_vigentes_soat: int;
    vencimiento_rtm: date;
    dias_vigentes_rtm: int;
    vencimiento_permiso: date;
    dias_vigentes_permiso: int;
    vencimiento_extintor: date;
    dias_vigentes_extintor: int;

class VehiclesUpdateSchema(BaseModel):
    id: int;
    ubicacion: str;
    placa: str;
    numero_motor: str;
    color_cabina: str;
    marca: str;
    linea: str;
    modelo: str;
    vencimiento_soat: date;
    dias_vigentes_soat: int;
    vencimiento_rtm: date;
    dias_vigentes_rtm: int;
    vencimiento_permiso: date;
    dias_vigentes_permiso: int;
    vencimiento_extintor: date;
    dias_vigentes_extintor: int;