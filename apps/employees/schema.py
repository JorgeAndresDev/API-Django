from pydantic import BaseModel

class EmployeeSchema(BaseModel):
    CC: int;
    NOM: str;
    CAR: str;
    CENTRO: str;
    CASH: str;
    SAC: str;
    CHECK: str;
    MOD: str;
    ER: str;
    PARADAS: str;
    PERFORMANCE: str;

class EmployeeCreateSchema(BaseModel):
    CC: int;
    NOM: str;
    CAR: str;
    CENTRO: str;

class UpdateEmployeeSchema(BaseModel):
    CC: int;
    NOM: str;
    CAR: str;
    CENTRO: str;