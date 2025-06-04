from pydantic import BaseModel

class CashlessSchema(BaseModel):
    CODIGO: int
    CLIENTE: str
    DT: str  # Cambiado de int a str para coincidir con la DB
    PLACA: str
    NUMERO: str  # Cambiado de str a int para coincidir con la DB
    NOVEDAD: str