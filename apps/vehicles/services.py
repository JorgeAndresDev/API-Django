import pandas as pd
from fastapi import HTTPException, UploadFile
from apps.vehicles.schemas import VehiclesCreateSchema, VehiclesUpdateSchema
from conexion.conexionBD import conexiondb

# Columnas requeridas en el Excel
COLUMNAS_REQUERIDAS = [
    "CD / UBICACIÓN", "PLACA / MATRÍCULA", "N° MOTOR", "COLOR (COLOR DE CABINA)", 
    "MARCA / FABRICANTE", "LINEA", "AÑO / MODELO ", 
    "Fecha de vencimiento", "DIAS PTES", "Fecha de vencimiento2",
    "DIAS PTES3", "Fecha de vencimiento4", "DIAS PTES5", "Fecha de vencimiento6",
    "DIAS PTES7"
]

# Mapeo de columnas del Excel a columnas de la BD
MAPEO_COLUMNAS = {
    "CD / UBICACIÓN": "ubicacion",
    "PLACA / MATRÍCULA": "placa",
    "N° MOTOR": "numero_motor",
    "COLOR (COLOR DE CABINA)": "color_cabina",
    "MARCA / FABRICANTE": "marca",
    "LINEA": "linea",
    "AÑO / MODELO ": "modelo",
    "Fecha de vencimiento": "vencimiento_soat",
    "DIAS PTES": "dias_vigentes_soat",
    "Fecha de vencimiento2": "vencimiento_rtm",
    "DIAS PTES3": "dias_vigentes_rtm",
    "Fecha de vencimiento4": "vencimiento_permiso",
    "DIAS PTES5": "dias_vigentes_permiso",
    "Fecha de vencimiento6": "vencimiento_extintor",
    "DIAS PTES7": "dias_vigentes_extintor"
}

def get_all_vehicles_service():     
    try:         
        connection = conexiondb()         
        if connection:             
            with connection.cursor(dictionary=True) as cursor:                 
                querySQL = """                     
                    SELECT   
                        id,                      
                        ubicacion,
                        placa,
                        numero_motor,
                        color_cabina,
                        marca,
                        linea,
                        modelo,
                        vencimiento_soat,
                        dias_vigentes_soat,
                        vencimiento_rtm,
                        dias_vigentes_rtm,
                        vencimiento_permiso,
                        dias_vigentes_permiso,
                        vencimiento_extintor,
                        dias_vigentes_extintor
                    FROM tbl_vehiculos                    
                    ORDER BY id DESC                 
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

def create_vehicle_service(vehicles_data: VehiclesCreateSchema):
    try:
        connection = conexiondb()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tbl_vehiculos (id, ubicacion, placa, numero_motor, color_cabina, marca, linea, modelo, vencimiento_soat, dias_vigentes_soat, vencimiento_rtm, dias_vigentes_rtm, vencimiento_permiso, dias_vigentes_permiso, vencimiento_extintor, dias_vigentes_extintor ) VALUES (%s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
               (vehicles_data.id, vehicles_data.ubicacion, vehicles_data.placa, vehicles_data.numero_motor, vehicles_data.color_cabina, vehicles_data.marca, vehicles_data.linea, vehicles_data.modelo, vehicles_data.vencimiento_soat, vehicles_data.dias_vigentes_soat, vehicles_data.vencimiento_rtm, vehicles_data.dias_vigentes_rtm, vehicles_data.vencimiento_permiso, vehicles_data.dias_vigentes_permiso, vehicles_data.vencimiento_extintor, vehicles_data.dias_vigentes_extintor))
        connection.commit()
        cursor.close()
        connection.close()
        if 'connection' in locals():
            connection.close()
        return {'success':True, "message": "Vehiculo creado Correctamente"}
    except Exception as e:
        return {"error": str(e)}
    
def update_vehicle_service(vehicle: VehiclesUpdateSchema):
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE tbl_vehiculos SET ubicacion = %s, placa = %s, numero_motor = %s, color_cabina = %s , marca = %s, linea = %s, modelo = %s, vencimiento_soat = %s, dias_vigentes_soat = %s, vencimiento_rtm = %s, dias_vigentes_rtm = %s, vencimiento_permiso = %s, dias_vigentes_permiso = %s, vencimiento_extintor = %s, dias_vigentes_extintor = %s WHERE id = %s",
                    (vehicle.ubicacion,vehicle.placa, vehicle.numero_motor, vehicle.color_cabina, vehicle.marca, vehicle.linea, vehicle.modelo, vehicle.vencimiento_soat, vehicle.dias_vigentes_soat, vehicle.vencimiento_rtm, vehicle.dias_vigentes_rtm, vehicle.vencimiento_permiso, vehicle.dias_vigentes_permiso, vehicle.vencimiento_extintor, vehicle.dias_vigentes_extintor, vehicle.id)
                )
                
                connection.commit()
                return {"message": "Conductor actualizado correctamente"}

        else:
            return {"error": "No se pudo establecer conexión con la base de datos"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'connection' in locals() and connection:
            connection.close()

async def upload_cashless(file: UploadFile):
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
        conn = conexiondb()
        if not conn:
            return {"error": "No se pudo conectar a la base de datos"}
        
        cursor = conn.cursor(dictionary=True)
        registros_actualizados = 0
        registros_insertados = 0

        # Insertar o actualizar datos en la BD
        for _, row in df.iterrows():
            # Convertir series de pandas a diccionario y garantizar tipos correctos
            vehiculos = row.to_dict()
            
            # Verificar si la cédula existe
            sql_check = "SELECT * FROM tbl_vehiculos WHERE placa = %s"
            cursor.execute(sql_check, (vehiculos["placa"],))
            vehiculos_existente = cursor.fetchone()

            if vehiculos_existente:
                # Actualizar vehiculos existente
                sql_update = """
                    UPDATE tbl_vehiculos SET 
                        ubicacion = %s,
                        numero_motor = %s,
                        color_cabina = %s, 
                        marca = %s, 
                        linea = %s, 
                        modelo = %s, 
                        vencimiento_soat = %s, 
                        dias_vigentes_soat = %s, 
                        vencimiento_rtm = %s,
                        dias_vigentes_rtm = %s,
                        vencimiento_permiso = %s,
                        dias_vigentes_permiso = %s,
                        vencimiento_extintor = %s,
                        dias_vigentes_extintor = %s
                    WHERE placa = %s
                """
                cursor.execute(sql_update, (
                    vehiculos["ubicacion"],
                    vehiculos["numero_motor"],
                    vehiculos["color_cabina"], 
                    vehiculos["marca"], 
                    vehiculos["linea"], 
                    vehiculos["modelo"], 
                    vehiculos["vencimiento_soat"], 
                    vehiculos["dias_vigentes_soat"], 
                    vehiculos["vencimiento_rtm"],
                    vehiculos["dias_vigentes_rtm"],
                    vehiculos["vencimiento_permiso"],
                    vehiculos["dias_vigentes_permiso"],
                    vehiculos["vencimiento_extintor"],
                    vehiculos["dias_vigentes_extintor"],
                    vehiculos["placa"]
                ))
                registros_actualizados += 1
            else:
                # Insertar nuevo vehiculos
                sql_insert = """
                    INSERT INTO tbl_vehiculos (
                        ubicacion, placa, numero_motor, color_cabina, marca, 
                        linea, modelo, vencimiento_soat, 
                        dias_vigentes_soat, vencimiento_rtm, dias_vigentes_rtm, vencimiento_permiso, dias_vigentes_permiso, vencimiento_extintor, dias_vigentes_extintor
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert, (
                    vehiculos["ubicacion"],
                    vehiculos["placa"], 
                    vehiculos["numero_motor"], 
                    vehiculos["color_cabina"], 
                    vehiculos["marca"], 
                    vehiculos["linea"], 
                    vehiculos["modelo"], 
                    vehiculos["vencimiento_soat"], 
                    vehiculos["dias_vigentes_soat"], 
                    vehiculos["vencimiento_rtm"],
                    vehiculos["dias_vigentes_rtm"],
                    vehiculos["vencimiento_permiso"],
                    vehiculos["dias_vigentes_permiso"],
                    vehiculos["vencimiento_extintor"],
                    vehiculos["dias_vigentes_extintor"],
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


async def delete_vehicle_service(id: int):
    try:
        conexion = conexiondb()
        if not conexion:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cursor = conexion.cursor()
        # Verificar si el conductor existe
        query_check = "SELECT * FROM tbl_vehiculos WHERE id = %s"
        cursor.execute(query_check, (id,))
        conductor = cursor.fetchone()
        if not conductor:
            raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

        # Eliminar el conductor
        query_delete = "DELETE FROM tbl_vehiculos WHERE id = %s"
        cursor.execute(query_delete, (id,))
        conexion.commit()
        cursor.close()
        conexion.close()

        return {"mensaje": "Vehiculo eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))