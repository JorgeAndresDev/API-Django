from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from conexion.conexionBD import conexiondb
from apps.cashless.schemas import CashlessSchema, UpdateCashlessSchema
from apps.cashless.services import get_all_cashless_service, update_cashless_service, upload_cashless_service




router = APIRouter(prefix="/cashless", tags=["Cashless"])

@router.get("/get_all_cashless")
async def get_all_cashless():
    try:
        cashless = get_all_cashless_service()
        if cashless is None:
            return JSONResponse({"error": "No se pudieron obtener los datos de cashless"}, status_code=500)
        return cashless
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/upload_cashless")
async def upload_cashless(file: UploadFile = File(...)):
    try:
        data = await upload_cashless_service(file)
        if "error" in data:
            return JSONResponse(data, status_code=400)
        return JSONResponse(data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/casless/update_cashless")
def update_cashless_endpoint(cashless: UpdateCashlessSchema):
    return update_cashless_service(cashless)