import datetime
from io import BytesIO
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
from apps.drivers.schemas import DriverCreateSchema
from apps.drivers.services import create_driver_service, delete_driver_service, get_all_drivers_service, upload_file_service

router = APIRouter(prefix="/drivers", tags=["Conductores"])

@router.get("/get_all_drivers")
async def get_all_drivers():
    try:
        # Obtener todos los conductores desde el servicio
        conductores = get_all_drivers_service()
        if conductores is None:
            return JSONResponse({"error": "No se pudieron obtener los conductores"}, status_code=500)
        return conductores
    except Exception as e:
        # Manejar errores y devolver una respuesta de error 500
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/create_driver")
async def create_driver(driver: DriverCreateSchema):
    try:
        response = create_driver_service(driver)
        return response
    except Exception as e:
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

@router.delete("/delete_drivers")
async def delete_driver(cedula: int):  # Cambiado a int para coincidir con el servicio
    try:
        resultado = await delete_driver_service(cedula)  # Agregado await
        return resultado
    except HTTPException as he:
        # Reenviar excepciones HTTP tal cual
        raise he
    except Exception as e:
        # Manejar otros errores y devolver una respuesta de error 500
        raise HTTPException(status_code=500, detail=str(e))