from pydantic import BaseModel

class CashlessSchema(BaseModel):
    CODIGO: int
    CLIENTE: str
    DT: str 
    PLACA: str
    NUMERO: str  
    NOVEDAD: str

class UpdateCashlessSchema(BaseModel):
    CODIGO: int
    NOVEDAD: str
