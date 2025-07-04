from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from apps.employees.schema import EmployeeCreateSchema, UpdateEmployeeSchema
from conexion.conexionBD import conexiondb
from apps.employees.services import create_employee_service, delete_empleado_services, download_employees_report_service, get_all_employees_service, update_employee_service, upload_cashless

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
        data = await upload_cashless(file)
        if "error" in data:
            return JSONResponse(data, status_code=400)
        return JSONResponse(data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/create_employee')
async def crear_empleado(employee: EmployeeCreateSchema):
    try:
            response = create_employee_service(employee)
            return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_employee/{CC}")
async def delete_empleado(CC: int):
    try:
        response = delete_empleado_services(CC)
        return response
    except Exception as e:
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

@router.get('/sql_detalles_empleadoBD')
async def sql_detalles_empleadoBD(cc: int):
    try:
        conexion = conexiondb()
        if not conexion:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cursor = conexion.cursor()
        query = "SELECT * FROM tbl_empleados WHERE cc = %s"
        cursor.execute(query, (cc,))
        empleado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
        return {"empleado": empleado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/update_employee')
async def update_employee(employee: UpdateEmployeeSchema):
    try:
        response = update_employee_service(employee)
        if not response:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
