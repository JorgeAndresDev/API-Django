from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from apps.cashless.services import get_all_cashless_service, upload_file_service


router = APIRouter(prefix="/casless", tags=["Cashless"])

@router.get("/get_all_cashless")
async def get_all_cashless():
    try:
        # Obtener todos los conductores desde el servicio
        cashless = get_all_cashless_service()
        if cashless is None:
            return JSONResponse({"error": "No se pudieron obtener los conductores"}, status_code=500)
        return cashless
    except Exception as e:
        # Manejar errores y devolver una respuesta de error 500
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    try:
        data = await upload_file_service(file)
        if "error" in data:
            return JSONResponse(data, status_code=400)
        return JSONResponse(data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))