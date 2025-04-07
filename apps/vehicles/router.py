from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from apps.vehicles.schemas import VehiclesCreateSchema, VehiclesUpdateSchema
from apps.vehicles.services import create_vehicle_service, delete_vehicle_service, get_all_vehicles_service, update_vehicle_service, upload_file_service

router = APIRouter(prefix="/vehicles", tags=["Vehiculos"])

@router.get("/get_all_vehicles")
async def get_all_vehicles():
    try:
        # Obtener todos los conductores desde el servicio
        conductores = get_all_vehicles_service()
        if conductores is None:
            return JSONResponse({"error": "No se pudieron obtener los conductores"}, status_code=500)
        return conductores
    except Exception as e:
        # Manejar errores y devolver una respuesta de error 500
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/create_vehicle")
async def create_vehicle(vehicle: VehiclesCreateSchema):
    try:
        response = create_vehicle_service(vehicle)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/update_vehicle")
async def update_vehicle(vehicle: VehiclesUpdateSchema):
    try:
        response = update_vehicle_service(vehicle)
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

@router.delete("/delete_vehicle/{id}")
async def delete_vehicle(id: int):
    try:
        resultado = await delete_vehicle_service(id)
        return resultado
    except HTTPException as he:
        raise he
    except Exception as e:  
        raise HTTPException(status_code=500, detail=str(e))