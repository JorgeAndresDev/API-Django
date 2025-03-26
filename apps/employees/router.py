from fastapi import FastAPI, UploadFile, File, APIRouter, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from conexion.conexionBD import connectionBD 

from apps.employees.services import get_all_employees_service





router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/get_all_employees")
async def get_all_employees():
    try:
        # Obtener todos los empleados desde el servicio
        employees = get_all_employees_service()
        return employees
    except Exception as e:
        # Manejar errores y devolver una respuesta de error 500
        raise HTTPException(status_code=500, detail=str(e))


app = FastAPI()

@router.post("/upload-employees-excel")
async def upload_employees_excel(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx o .xls)")
    
    try:
        df = pd.read_excel(file.file)
        df = df.fillna(0) 

        conn = connectionBD()
        cursor = conn.cursor(dictionary=True)

        for _, row in df.iterrows():
            # Verificar si el empleado existe
            sql_check = "SELECT * FROM tbl_empleados WHERE CC = %s"
            cursor.execute(sql_check, (row["CC"],))
            employee_exists = cursor.fetchone()

            if employee_exists:
                # Actualizar empleado existente
                sql_update = """
                    UPDATE tbl_empleados SET NOM = %s, CAR = %s, CENTRO = %s, CASH = %s, 
                    SAC = %s, `CHECK` = %s, `MOD` = %s, ER = %s, PARADAS = %s, PERFORMANCE = %s 
                    WHERE CC = %s
                """
                cursor.execute(sql_update, (
                    row["NOM"], row["CAR"], row["CENTRO"], row["CASH"], 
                    row["SAC"], row["CHECK"], row["MOD"], row["ER"], 
                    row["PARADAS"], row["PERFORMANCE"], row["CC"]
                ))
            else:
                # Insertar nuevo empleado
                sql_insert = """
                    INSERT INTO tbl_empleados 
                    (CC, NOM, CAR, CENTRO, CASH, SAC, `CHECK`, `MOD`, ER, PARADAS, PERFORMANCE)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert, (
                    row["CC"], row["NOM"], row["CAR"], row["CENTRO"], row["CASH"], 
                    row["SAC"], row["CHECK"], row["MOD"], row["ER"], 
                    row["PARADAS"], row["PERFORMANCE"]
                ))
            
            conn.commit()

        cursor.close()
        conn.close()
        
        return JSONResponse(
            status_code=200,
            content={"message": "Base de datos actualizada correctamente"}
        )

    except Exception as e:
        # Manejo de errores genéricos
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el archivo: {str(e)}"
        )