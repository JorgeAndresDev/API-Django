import datetime
from io import BytesIO
from flask import make_response
import pandas as pd
from fastapi import UploadFile
from conexion.conexionBD import conexiondb

def procesar_form_inspeccion_botiquin(dataForm):
    try:
        with conexiondb() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                INSERT INTO inspecciones_botiquines (
                    placa_vehiculo, gasas_limpias, esparadrapo_tela, baja_lenguas,
                    guantes_latex, venda_elastica_2, venda_elastica_3, venda_elastica_5,
                    venda_algodon, yodopovidona, solucion_salina, termometro_digital,
                    alcohol_antiseptico, botella_agua, bandas_adhesivas, tijeras_punta_roma,
                    pito_emergencias, manual_primeros_auxilios, observaciones
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                valores = (
                    dataForm.get('placa_vehiculo'),
                    dataForm.get('gasas_limpias'),
                    dataForm.get('esparadrapo_tela'),
                    dataForm.get('baja_lenguas'),
                    dataForm.get('guantes_latex'),
                    dataForm.get('venda_elastica_2'),
                    dataForm.get('venda_elastica_3'),
                    dataForm.get('venda_elastica_5'),
                    dataForm.get('venda_algodon'),
                    dataForm.get('yodopovidona'),
                    dataForm.get('solucion_salina'),
                    dataForm.get('termometro_digital'),
                    dataForm.get('alcohol_antiseptico'),
                    dataForm.get('botella_agua'),
                    dataForm.get('bandas_adhesivas'),
                    dataForm.get('tijeras_punta_roma'),
                    dataForm.get('pito_emergencias'),
                    dataForm.get('manual_primeros_auxilios'),
                    dataForm.get('observaciones', '')  # Valor por defecto si falta
                )
                
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.rowcount  # Devuelve el número de filas afectadas
    except Exception as e:
        print(f"Error en procesar_form_inspeccion: {e}")
        return None

def sql_lista_inspeccionesBD():
    """
    Obtiene la lista de inspecciones desde la base de datos.
    """
    try:
        with conexiondb() as conexion_MySQLdb:  # Abre la conexión
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:  # Obtiene el cursor
                querySQL = """
                SELECT 
                    id_inspeccion,
                    placa_vehiculo,
                    gasas_limpias,
                    esparadrapo_tela,
                    baja_lenguas,
                    guantes_latex,
                    venda_elastica_2,
                    venda_elastica_3,
                    venda_elastica_5,
                    venda_algodon,
                    yodopovidona,
                    solucion_salina,
                    termometro_digital,
                    alcohol_antiseptico,
                    botella_agua,
                    bandas_adhesivas,
                    tijeras_punta_roma,
                    pito_emergencias,
                    manual_primeros_auxilios,
                    observaciones,
                    DATE_FORMAT(fecha_inspeccion, '%Y-%m-%d %H:%i') AS fecha_inspeccion
                FROM inspecciones_botiquines
                ORDER BY id_inspeccion DESC
                """
                cursor.execute(querySQL)  # ✅ EJECUTAR LA CONSULTA CON EL CURSOR
                resultados = cursor.fetchall()  # ✅ OBTENER LOS DATOS
                
                if not resultados:
                    print("🔍 No se encontraron datos en la tabla inspecciones_botiquines.")

                return resultados
    except Exception as e:
        print(f"❌ Error en sql_lista_inspeccionesBD: {e}")
        return None

def procesar_form_inspeccion_botiquin(dataForm):
    """
    Inserta una nueva inspección en la base de datos.
    """
    try:
        with conexiondb() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                INSERT INTO inspecciones_botiquines (
                    placa_vehiculo, gasas_limpias, esparadrapo_tela, baja_lenguas,
                    guantes_latex, venda_elastica_2, venda_elastica_3, venda_elastica_5,
                    venda_algodon, yodopovidona, solucion_salina, termometro_digital,
                    alcohol_antiseptico, botella_agua, bandas_adhesivas, tijeras_punta_roma,
                    pito_emergencias, manual_primeros_auxilios, observaciones
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                valores = (
                    dataForm['placa_vehiculo'],
                    dataForm['gasas_limpias'],
                    dataForm['esparadrapo_tela'],
                    dataForm['baja_lenguas'],
                    dataForm['guantes_latex'],
                    dataForm['venda_elastica_2'],
                    dataForm['venda_elastica_3'],
                    dataForm['venda_elastica_5'],
                    dataForm['venda_algodon'],
                    dataForm['yodopovidona'],
                    dataForm['solucion_salina'],
                    dataForm['termometro_digital'],
                    dataForm['alcohol_antiseptico'],
                    dataForm['botella_agua'],
                    dataForm['bandas_adhesivas'],
                    dataForm['tijeras_punta_roma'],
                    dataForm['pito_emergencias'],
                    dataForm['manual_primeros_auxilios'],
                    dataForm.get('observaciones', '')  # Si no hay observaciones, usa un string vacío
                )
                
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()

                if cursor.rowcount > 0:
                    return {"id_insertado": cursor.lastrowid, "mensaje": "Inspección registrada con éxito"}
                else:
                    return {"error": "No se pudo insertar la inspección"}

    except Exception as e:
        print(f"❌ Error en procesar_form_inspeccion_botiquin: {e}")
        return {"error": str(e)}

def sql_detalles_inspeccionBD(id_inspeccion: int):
    """
    Obtiene los detalles de una inspección específica en la base de datos.
    """
    try:
        with conexiondb() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                SELECT 
                    id_inspeccion,
                    placa_vehiculo,
                    gasas_limpias,
                    esparadrapo_tela,
                    baja_lenguas,
                    guantes_latex,
                    venda_elastica_2,
                    venda_elastica_3,
                    venda_elastica_5,
                    venda_algodon,
                    yodopovidona,
                    solucion_salina,
                    termometro_digital,
                    alcohol_antiseptico,
                    botella_agua,
                    bandas_adhesivas,
                    tijeras_punta_roma,
                    pito_emergencias,
                    manual_primeros_auxilios,
                    observaciones,
                    DATE_FORMAT(fecha_inspeccion, '%Y-%m-%d %H:%i') AS fecha_inspeccion
                FROM inspecciones_botiquines
                WHERE id_inspeccion = %s
                """
                cursor.execute(querySQL, (id_inspeccion,))
                detalles = cursor.fetchone()
                
                return detalles if detalles else None
    except Exception as e:
        print(f"❌ Error en sql_detalles_inspeccionBD: {e}")
        return None

def procesar_actualizacion_inspeccion(dataForm):
    try:
        with conexiondb() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                UPDATE inspecciones_botiquines SET
                    placa_vehiculo = %s,
                    gasas_limpias = %s,
                    esparadrapo_tela = %s,
                    baja_lenguas = %s,
                    guantes_latex = %s,
                    venda_elastica_2 = %s,
                    venda_elastica_3 = %s,
                    venda_elastica_5 = %s,
                    venda_algodon = %s,
                    yodopovidona = %s,
                    solucion_salina = %s,
                    termometro_digital = %s,
                    alcohol_antiseptico = %s,
                    botella_agua = %s,
                    bandas_adhesivas = %s,
                    tijeras_punta_roma = %s,
                    pito_emergencias = %s,
                    manual_primeros_auxilios = %s,
                    observaciones = %s
                WHERE id_inspeccion = %s
                """
                
                valores = (
                    dataForm['placa_vehiculo'],
                    dataForm['gasas_limpias'],
                    dataForm['esparadrapo_tela'],
                    dataForm['baja_lenguas'],
                    dataForm['guantes_latex'],
                    dataForm['venda_elastica_2'],
                    dataForm['venda_elastica_3'],
                    dataForm['venda_elastica_5'],
                    dataForm['venda_algodon'],
                    dataForm['yodopovidona'],
                    dataForm['solucion_salina'],
                    dataForm['termometro_digital'],
                    dataForm['alcohol_antiseptico'],
                    dataForm['botella_agua'],
                    dataForm['bandas_adhesivas'],
                    dataForm['tijeras_punta_roma'],
                    dataForm['pito_emergencias'],
                    dataForm['manual_primeros_auxilios'],
                    dataForm.get('observaciones', ''),  # Si no hay observaciones, se usa ''
                    dataForm['id_inspeccion']
                )
                
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"Error en procesar_actualizacion_inspeccion: {e}")
        return None

def eliminarInspeccion(id_inspeccion):
    try:
        with conexiondb() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM inspecciones_botiquines WHERE id_inspeccion = %s"
                cursor.execute(querySQL, (id_inspeccion,))
                conexion_MySQLdb.commit()
                if cursor.rowcount > 0:
                    return {"success": True, "message": "Inspección eliminada correctamente"}
                else:
                    return {"success": False, "error": "No se encontró la inspección para eliminar"}
    except Exception as e:
        print(f"Error en eliminarInspeccion: {e}")
        return {"success": False, "error": str(e)}




