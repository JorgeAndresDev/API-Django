from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse


from apps.employees.services import get_all_employees_service, upload_file_service

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/get_all_employees")
async def get_all_employees():
    try:
        # Obtener todos los productos desde el servicio
        employees = get_all_employees_service()
        return employees
    except Exception as e:
        # Manejar errores y devolver una respuesta de error 500
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    try:
        data = upload_file_service(file)
        
        if "error" in data:
            return JSONResponse(data, status_code=400)
        return JSONResponse(data, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
