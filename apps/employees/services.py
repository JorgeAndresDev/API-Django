import datetime
from io import BytesIO
from flask import make_response
import pandas as pd
from fastapi import HTTPException, UploadFile
from conexion.conexionBD import conexiondb


def get_all_employees_service():     
    try:         
        connection = conexiondb()         
        if connection:             
            with connection.cursor(dictionary=True) as cursor:                 
                querySQL = """                     
                    SELECT                         
                        CC,                         
                        NOM,                         
                        CAR,                         
                        CENTRO                                            
                    FROM tbl_empleados                     
                    ORDER BY CC DESC                 
                """                 
                cursor.execute(querySQL)                 
                empleadosBD = cursor.fetchall()                 
                return empleadosBD         
        else:             
            return None     
    except Exception as e:         
        print(f"Error en la función sql_lista_empleadosBD: {e}")         
        return None     
    finally:         
        if connection:             
            connection.close()

async def upload_file_service(file: UploadFile):
    try:
        # Volver a posicionar el puntero para leer el archivo
        file.file.seek(0)
        df = pd.read_excel(file.file)  # Convertirlo en DataFrame

        # Verificar si está vacío
        if df.empty:
            return {"error": "El archivo está vacío"}

        df.fillna(0, inplace=True)  # Reemplazar NaN por 0

        # Conectar a la BD
        conn = conexiondb()
        if not conn:
            return {"error": "No se pudo conectar a la base de datos"}
        
        cursor = conn.cursor(dictionary=True)

        # Insertar o actualizar datos en la BD
        for _, row in df.iterrows():
            sql_check = "SELECT * FROM tbl_empleados WHERE CC = %s"
            cursor.execute(sql_check, (row["CC"],))
            empleado_existente = cursor.fetchone()

            if empleado_existente:
                sql_update = """
                    UPDATE tbl_empleados SET NOM = %s, CAR = %s, CENTRO = %s, CASH = %s, 
                    SAC = %s, `CHECK` = %s, `MOD` = %s, ER = %s, PARADAS = %s, PERFORMANCE = %s 
                    WHERE CC = %s
                """
                cursor.execute(sql_update, (
                    row["NOM"], row["CAR"], row["CENTRO"], row["CASH"], row["SAC"], 
                    row["CHECK"], row["MOD"], row["ER"], row["PARADAS"], row["PERFORMANCE"], row["CC"]
                ))
            else:
                sql_insert = """
                    INSERT INTO tbl_empleados (CC, NOM, CAR, CENTRO, CASH, SAC, `CHECK`, `MOD`, ER, PARADAS, PERFORMANCE)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert, (
                    row["CC"], row["NOM"], row["CAR"], row["CENTRO"], row["CASH"], 
                    row["SAC"], row["CHECK"], row["MOD"], row["ER"], row["PARADAS"], row["PERFORMANCE"]
                ))

        conn.commit()  # Guardar cambios
        cursor.close()
        conn.close()

        return {"success": True, "message": "Base de datos actualizada correctamente"}

    except Exception as e:
        return {"error": str(e)}


async def delete_employee_service(cc: int):
    try:
        conexion = conexiondb()
        if not conexion:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cursor = conexion.cursor()
        # Verificar si el empleado existe
        query_check = "SELECT * FROM tbl_empleados WHERE cc = %s"
        cursor.execute(query_check, (cc,))
        empleado = cursor.fetchone()
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        # Eliminar el empleado
        query_delete = "DELETE FROM tbl_empleados WHERE cc = %s"
        cursor.execute(query_delete, (cc,))
        conexion.commit()
        cursor.close()
        conexion.close()

        return {"mensaje": "Empleado eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))