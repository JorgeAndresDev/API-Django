from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from conexion.conexionBD import conexiondb



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
        data = await upload_file_service(file)
        if "error" in data:
            return JSONResponse(data, status_code=400)
        return JSONResponse(data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/empleados/{cc}")
async def eliminar_empleado(cc: int):
    try:
        conexion = conexiondb()
        if not conexion:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cursor = conexion.cursor()
        query = "DELETE FROM tbl_empleados WHERE cc = %s"
        cursor.execute(query, (cc,))
        conexion.commit()
        cursor.close()
        conexion.close()

        return {"mensaje": "Empleado eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))