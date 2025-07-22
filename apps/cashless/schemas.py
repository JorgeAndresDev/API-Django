from pydantic import BaseModel, Field


class CashlessSchema(BaseModel):
    codigo_cliente: int = Field(alias="CODIGO")
    cliente_nombre: str = Field(alias="CLIENTE") 
    Documento_pedido: int = Field(alias="DT")
    placa_vehiculo: str = Field(alias="PLACA")
    numero_cliente: int = Field(alias="NUMERO") 
    Novedad: str = Field(alias="NOVEDAD")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True  # Para Pydantic v2

class UpdateCashlessSchema(BaseModel):
    codigo_cliente: int = Field(alias="CODIGO")
    Novedad: str = Field(alias="NOVEDAD")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True  # Para Pydantic v2

