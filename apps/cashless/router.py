from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from conexion.conexionBD import conexiondb
from apps.cashless.schemas import UpdateCashlessSchema
from apps.cashless.services import delete_cashless_services, get_all_cashless_service, update_cashless_service, upload_cashless_service


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
    
@router.post("/upload_file")
async def upload_cashless(file: UploadFile = File(...)):
    try:
        data = await upload_cashless_service(file)
        if "error" in data:
            return JSONResponse(data, status_code=400)
        return JSONResponse(data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/update_client")
async def update_cashless(cashless: UpdateCashlessSchema):
    try:
        response = update_cashless_service(cashless)
        if not response:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_cashless/{codigo_cliente}")
async def delete_empleado(codigo_cliente: int):
    try:
        response = delete_cashless_services(codigo_cliente=codigo_cliente)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))