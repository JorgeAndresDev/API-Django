import pandas as pd
from fastapi import HTTPException, UploadFile
from apps.drivers.schemas import DriverCreateSchema
from conexion.conexionW.conexionBDW import conexiondbw

# Columnas requeridas en el Excel
COLUMNAS_REQUERIDAS = [
    "NOMBRES Y APELLIDOS", "NÚMERO DE IDENTIFICACIÓN", "CARGO", "FECHA VENCIMIENTO LICENCIA", 
    "DÍAS PTES LICENCIA", "COMPARENDOS", "ACUERDO DE PAGO", 
    "FECHA VENCIMIENTO CURSO", "DÍAS PTES CURSO"
]

# Mapeo de columnas del Excel a columnas de la BD
MAPEO_COLUMNAS = {
    "NOMBRES Y APELLIDOS": "nombre_apellido",
    "NÚMERO DE IDENTIFICACIÓN": "cedula",
    "CARGO": "cargo",
    "FECHA VENCIMIENTO LICENCIA": "vencimiento_licencia",
    "DÍAS PTES LICENCIA": "dias_restantes_licencia",
    "COMPARENDOS": "comparendos",
    "ACUERDO DE PAGO": "acuerdo_pago",
    "FECHA VENCIMIENTO CURSO": "vencimiento_curso",
    "DÍAS PTES CURSO": "dias_restantes_curso"
}

def get_all_drivers_service():     
    try:         
        connection = conexiondbw()         
        if connection:             
            with connection.cursor(dictionary=True) as cursor:                 
                querySQL = """                     
                    SELECT                         
                        cedula,                    
                        nombre_apellido,   
                        cargo,
                        vencimiento_licencia,
                        dias_restantes_licencia,
                        comparendos,
                        acuerdo_pago,
                        vencimiento_curso,
                        dias_restantes_curso
                    FROM tbl_conductores                    
                    ORDER BY cedula DESC                 
                """                 
                cursor.execute(querySQL)                 
                conductoresBD = cursor.fetchall()                 
                return conductoresBD         
        else:             
            return None     
    except Exception as e:         
        print(f"Error en la función sql_lista_conductoresBD: {e}")         
        return None     
    finally:         
        if connection:             
            connection.close()

def create_driver_service(driver_data: DriverCreateSchema):
    try:
        connection = conexiondbw()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tbl_conductores (cedula, nombre_apellido, cargo, vencimiento_licencia, dias_restantes_licencia, comparendos, acuerdo_pago, vencimiento_curso, dias_restantes_curso) VALUES (%s, %s, %s , %s, %s, %s, %s, %s, %s)", 
               (driver_data.cedula, driver_data.nombre_apellido, driver_data.cargo, driver_data.vencimiento_licencia, driver_data.dias_restantes_licencia, driver_data.comparendos, driver_data.acuerdo_pago, driver_data.vencimiento_curso, driver_data.dias_restantes_curso ))
        connection.commit()
        cursor.close()
        connection.close()
        if 'connection' in locals():
            connection.close()
        return {'success':True, "message": "Usuario creado Correctamente"}
    except Exception as e:
        return {"error": str(e)}

async def upload_file_service(file: UploadFile):
    try:
        # Volver a posicionar el puntero para leer el archivo
        file.file.seek(0)
        df = pd.read_excel(file.file)  # Convertirlo en DataFrame

        # Verificar si está vacío
        if df.empty:
            return {"error": "El archivo está vacío"}

        # Verificar que estén todas las columnas requeridas
        columnas_faltantes = [col for col in COLUMNAS_REQUERIDAS if col not in df.columns]
        if columnas_faltantes:
            return {
                "error": f"Faltan columnas requeridas en el archivo: {', '.join(columnas_faltantes)}",
                "columnas_requeridas": COLUMNAS_REQUERIDAS
            }

        # Filtrar solo las columnas que necesitamos
        df = df[COLUMNAS_REQUERIDAS]
        
        # Reemplazar NaN por 0
        df.fillna(0, inplace=True)
        
        # Renombrar las columnas según el mapeo
        df.rename(columns=MAPEO_COLUMNAS, inplace=True)

        # Conectar a la BD
        conn = conexiondbw()
        if not conn:
            return {"error": "No se pudo conectar a la base de datos"}
        
        cursor = conn.cursor(dictionary=True)
        registros_actualizados = 0
        registros_insertados = 0

        # Insertar o actualizar datos en la BD
        for _, row in df.iterrows():
            # Convertir series de pandas a diccionario y garantizar tipos correctos
            conductor = row.to_dict()
            
            # Verificar si la cédula existe
            sql_check = "SELECT * FROM tbl_conductores WHERE cedula = %s"
            cursor.execute(sql_check, (conductor["cedula"],))
            conductor_existente = cursor.fetchone()

            if conductor_existente:
                # Actualizar conductor existente
                sql_update = """
                    UPDATE tbl_conductores SET 
                        nombre_apellido = %s,
                        cargo = %s, 
                        vencimiento_licencia = %s, 
                        dias_restantes_licencia = %s, 
                        comparendos = %s, 
                        acuerdo_pago = %s, 
                        vencimiento_curso = %s, 
                        dias_restantes_curso = %s
                    WHERE cedula = %s
                """
                cursor.execute(sql_update, (
                    conductor["nombre_apellido"],
                    conductor["cargo"], 
                    conductor["vencimiento_licencia"], 
                    conductor["dias_restantes_licencia"], 
                    conductor["comparendos"], 
                    conductor["acuerdo_pago"], 
                    conductor["vencimiento_curso"], 
                    conductor["dias_restantes_curso"],
                    conductor["cedula"]
                ))
                registros_actualizados += 1
            else:
                # Insertar nuevo conductor
                sql_insert = """
                    INSERT INTO tbl_conductores (
                        nombre_apellido, cedula, cargo, vencimiento_licencia, 
                        dias_restantes_licencia, comparendos, acuerdo_pago, 
                        vencimiento_curso, dias_restantes_curso
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert, (
                    conductor["nombre_apellido"],
                    conductor["cedula"], 
                    conductor["cargo"], 
                    conductor["vencimiento_licencia"], 
                    conductor["dias_restantes_licencia"], 
                    conductor["comparendos"], 
                    conductor["acuerdo_pago"], 
                    conductor["vencimiento_curso"], 
                    conductor["dias_restantes_curso"]
                ))
                registros_insertados += 1

        conn.commit()  # Guardar cambios
        cursor.close()
        conn.close()

        return {
            "success": True, 
            "message": f"Base de datos actualizada correctamente. {registros_insertados} registros insertados, {registros_actualizados} registros actualizados."
        }

    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        return {"error": str(e), "detail": error_detail}


async def delete_driver_service(cc: int):
    try:
        conexion = conexiondbw()
        if not conexion:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cursor = conexion.cursor()
        # Verificar si el conductor existe
        query_check = "SELECT * FROM tbl_conductores WHERE cedula = %s"
        cursor.execute(query_check, (cc,))
        conductor = cursor.fetchone()
        if not conductor:
            raise HTTPException(status_code=404, detail="Conductor no encontrado")

        # Eliminar el conductor
        query_delete = "DELETE FROM tbl_conductores WHERE cedula = %s"
        cursor.execute(query_delete, (cc,))
        conexion.commit()
        cursor.close()
        conexion.close()

        return {"mensaje": "Conductor eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))