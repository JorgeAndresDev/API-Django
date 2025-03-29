from fastapi import File, UploadFile
from conexion import conexionBD
from conexion.conexionBD import connectionBD 
from flask import jsonify, request
import pandas as pd
from io import BytesIO


def get_all_employees_service():     
    try:         
        connection = connectionBD()         
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

 

def upload_file_service(file: UploadFile):
    try:
        # Volver a posicionar el puntero para leer el archivo
        file.file.seek(0)
        df = pd.read_excel(file.file)  # Convertirlo en DataFrame

        # Verificar si el archivo está vacío
        if df.empty:
            return {"error": "El archivo está vacío"}

        # Reemplazar NaN por 0
        df = df.fillna(0)

        # Conectar a la base de datos
        conn = conexionBD()
        cursor = conn.cursor(dictionary=True)

        # Iterar sobre las filas del DataFrame
        for _, row in df.iterrows():
            sql_check = "SELECT * FROM tbl_empleados WHERE CC = %s"
            cursor.execute(sql_check, (row["CC"],))
            empleado_existente = cursor.fetchone()

            if empleado_existente:
                # Si el empleado existe, actualizar sus datos
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
                # Si el empleado no existe, insertarlo
                sql_insert = """
                    INSERT INTO tbl_empleados (CC, NOM, CAR, CENTRO, CASH, SAC, `CHECK`, `MOD`, ER, PARADAS, PERFORMANCE)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert, (
                    row["CC"], row["NOM"], row["CAR"], row["CENTRO"], row["CASH"], 
                    row["SAC"], row["CHECK"], row["MOD"], row["ER"], row["PARADAS"], row["PERFORMANCE"]
                ))
            
            conn.commit()  # Guardar cambios en la BD

        # Cerrar conexión
        cursor.close()
        conn.close()

        return {"message": "Base de datos actualizada correctamente", "success": True}

    except Exception as e:
        return {"error": str(e)}
