from fastapi import File, UploadFile
from conexion import conexionBD 
from flask import jsonify, request
import pandas as pd
from io import BytesIO
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
        # Leer el archivo
        file_contents = await file.read()
        df = pd.read_excel(BytesIO(file_contents))

        # Verificar si está vacío
        if df.empty:
            return {"error": "El archivo está vacío"}

        df.fillna(0, inplace=True)  # Reemplazar NaN por 0

        # Conectar a la BD
        conn = conexionBD()
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

        return {"message": "Base de datos actualizada correctamente", "success": True}

    except Exception as e:
        return {"error": str(e)}



def eliminar_empleado(cc: int):
    conexion = conexionBD()
    if not conexion:
        return {"error": "Error de conexión a la base de datos"}

    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM tbl_empleados WHERE cc = %s", (cc,))
        conexion.commit()

        if cursor.rowcount == 0:
            return {"error": "Empleado no encontrado"}

        return {"mensaje": "Empleado eliminado correctamente"}

    except Exception as e:
        return {"error": f"Error al eliminar empleado: {str(e)}"}

    finally:
        cursor.close()
        conexion.close()