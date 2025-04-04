from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from conexion.conexionBD import conexiondb
from apps.employees.services import download_employees_report_service, get_all_employees_service, upload_file_service

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


@router.post('/crear_empleado')
async def crear_empleado(cc: int, nom: str, car: str, centro: str):
    try:
        conexion = conexiondb()
        if not conexion:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cursor = conexion.cursor()
        query = """
            INSERT INTO tbl_empleados (cc, nom, car, centro)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (cc, nom, car, centro))
        conexion.commit()
        cursor.close()
        conexion.close()

        return {"mensaje": "Empleado creado exitosamente"}
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

@router.put('/actualizar_empleadoBD')
async def actualizar_empleadoBD(cc: int, nom: str = None, car: str = None, centro: str = None):
    try:
        conexion = conexiondb()
        if not conexion:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cursor = conexion.cursor()
        query = "UPDATE tbl_empleados SET "
        updates = []
        params = []

        if nom:
            updates.append("nom = %s")
            params.append(nom)
        if car:
            updates.append("car = %s")
            params.append(car)
        if centro:
            updates.append("centro = %s")
            params.append(centro)

        if not updates:
            raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")

        query += ", ".join(updates) + " WHERE cc = %s"
        params.append(cc)

        cursor.execute(query, tuple(params))
        conexion.commit()
        cursor.close()
        conexion.close()

        return {"mensaje": "Empleado actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
