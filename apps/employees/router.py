import datetime
from io import BytesIO
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
<<<<<<< HEAD
from flask import make_response
import pandas as pd
from apps.employees.services import delete_employee_service, get_all_employees_service, upload_file_service
from conexion.conexionBD import conexiondb
=======
from conexion.conexionBD import conexiondb
from apps.employees.services import download_employees_report_service, get_all_employees_service, upload_file_service
>>>>>>> 32cb5158661a4154c9dbf0b485c5ef15d8fe4db7

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
        data = await upload_file_service(file)
        if "error" in data:
            return JSONResponse(data, status_code=400)
        return JSONResponse(data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_employee/{cc}")
async def delete_employee(cc: str):
    try:
        employees = delete_employee_service(cc)
        return employees
    except Exception as e:
<<<<<<< HEAD
        # Manejar errores y devolver una respuesta de error 500
        raise HTTPException(status_code=500, detail=str(e))
=======
        raise HTTPException(status_code=500, detail=str(e))
    
    
from fastapi.responses import FileResponse

@router.get('/descargar-informe-empleados')
async def descargar_informe_empleados():
    try:
        output, filename = download_employees_report_service()  # output debe ser BytesIO
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
>>>>>>> 32cb5158661a4154c9dbf0b485c5ef15d8fe4db7
