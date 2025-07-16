import datetime
from io import BytesIO
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
from apps.drivers.schemas import DriverCreateSchema, DriverUpdateSchema
from apps.drivers.services import create_driver_service, delete_driver_service, get_all_drivers_service, update_driver_service,  upload_driver

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
    
@router.put("/update_driver")
async def update_driver(driver: DriverUpdateSchema):
    try:
        response = update_driver_service(driver)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    try:
        data = await upload_driver(file)
        if "error" in data:
            return JSONResponse(data, status_code=400)
        return JSONResponse(data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_driver/{id_conductor}")
async def delete_driver(id_conductor: int):
    try:
        resultado = await delete_driver_service(id_conductor)
        return resultado
    except HTTPException as he:
        raise he
    except Exception as e:  
        raise HTTPException(status_code=500, detail=str(e))