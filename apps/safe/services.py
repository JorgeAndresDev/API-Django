import datetime
from io import BytesIO
from flask import make_response
import pandas as pd
from fastapi import UploadFile
from conexion.conexionBD import conexiondb

def procesar_form_inspeccion_caja(dataForm):
    try:
        # Validación de campos requeridos
        campos_requeridos = [
            'placa_vehiculo', 'puerta_estado', 'puerta_facilidad',
            'clave_precisa', 'clave_autorizada', 'perilla_funciona',
            'numeros_visibles', 'caja_anclada'
        ]
        
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo]:
                raise ValueError(f"El campo {campo} es requerido")

        with conexiondb() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """INSERT INTO inspeccion_cajas_fuertes 
                        (placa_vehiculo, puerta_estado, puerta_facilidad, clave_precisa, 
                         clave_autorizada, perilla_funciona, numeros_visibles, 
                         caja_anclada, observaciones) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

                # Manejo de observaciones (puede ser NULL)
                observaciones = dataForm['observaciones'] if 'observaciones' in dataForm and dataForm['observaciones'] else None

                valores = (
                    dataForm['placa_vehiculo'].strip().upper(),  # Normalización de placa
                    dataForm['puerta_estado'],
                    dataForm['puerta_facilidad'],
                    dataForm['clave_precisa'],
                    dataForm['clave_autorizada'],
                    dataForm['perilla_funciona'],
                    dataForm['numeros_visibles'],
                    dataForm['caja_anclada'],
                    observaciones  # Manejo de NULL
                )
                
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                
                if cursor.rowcount == 1:
                    return cursor.lastrowid  # Retorna el ID insertado
                return None

    except Exception as e:
        print(f"Error en procesar_form_inspeccion_caja: {str(e)}")
        if 'conexion_MySQLdb' in locals():
            conexion_MySQLdb.rollback()
        return None



def obtener_inspecciones_cajas():
    import traceback
    try:
        with conexiondb() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        id_inspeccion_cf AS id_inspeccion,
                        placa_vehiculo,
                        puerta_estado,
                        puerta_facilidad,
                        clave_precisa,
                        clave_autorizada,
                        perilla_funciona,
                        numeros_visibles,
                        caja_anclada,
                        observaciones,
                        DATE_FORMAT(fecha_inspeccion, '%Y-%m-%d %H:%i') AS fecha_inspeccion_formateada
                    FROM inspeccion_cajas_fuertes
                    ORDER BY fecha_inspeccion DESC
                """
                cursor.execute(querySQL)
                resultados = cursor.fetchall()
                print("Resultados:", resultados)
                return resultados
    except Exception as e:
        print("Error en obtener_inspecciones_cajas:")
        traceback.print_exc()
        return None



    
def obtener_detalle_inspeccion(id_inspeccion_cf):
    try:
        with conexiondb() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        id_inspeccion_cf,
                        placa_vehiculo,
                        puerta_estado,
                        puerta_facilidad,
                        clave_precisa,
                        clave_autorizada,
                        perilla_funciona,
                        numeros_visibles,
                        caja_anclada,
                        observaciones,
                        IFNULL(DATE_FORMAT(fecha_inspeccion, '%d/%m/%Y %H:%i'), 'No registrada') AS fecha_inspeccion_formateada,
                        fecha_inspeccion
                    FROM inspeccion_cajas_fuertes
                    WHERE id_inspeccion_cf = %s
                """
                cursor.execute(querySQL, (id_inspeccion_cf,))
                return cursor.fetchone()
    except Exception as e:
        print(f"Error en obtener_detalle_inspeccion: {str(e)}")
        return None
    

def eliminar_inspeccion_cf(id_inspeccion_cf: int):
    try:
        connectado = conexiondb()  # Conexión a la base de datos
        if connectado:
            with connectado.cursor() as cursor:
                # Consulta para eliminar la inspección
                cursor.execute("DELETE FROM inspeccion_cajas_fuertes WHERE id_inspeccion_cf = %s", (id_inspeccion_cf,))
                connectado.commit()
                # Verificar si se eliminó alguna fila
                if cursor.rowcount > 0:
                    return {'success': True, 'message': 'Inspección eliminada correctamente'}
                else:
                    return {'success': False, 'message': 'Inspección no encontrada'}
        else:
            return {'success': False, 'message': 'Error al conectar a la base de datos'}
    except Exception as e:
        print(f"Error en eliminar_inspeccion_cf: {str(e)}")
        return {'success': False, 'error': str(e)}
    finally:
        if 'connectado' in locals() and connectado:
            connectado.close()
# Función para actualizar inspección
def actualizar_inspeccion_bd(id_inspeccion_cf, data_form):
    try:
        campos_requeridos = [
            'placa_vehiculo', 'puerta_estado', 'puerta_facilidad',
            'clave_precisa', 'clave_autorizada', 'perilla_funciona',
            'numeros_visibles', 'caja_anclada'
        ]
        
        # Validar campos requeridos
        for campo in campos_requeridos:
            if campo not in data_form or not data_form[campo]:
                return {'success': False, 'message': f'El campo {campo} es requerido'}

        with conexiondb() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    UPDATE inspeccion_cajas_fuertes 
                    SET 
                        placa_vehiculo = %s,
                        puerta_estado = %s,
                        puerta_facilidad = %s,
                        clave_precisa = %s,
                        clave_autorizada = %s,
                        perilla_funciona = %s,
                        numeros_visibles = %s,
                        caja_anclada = %s,
                        observaciones = %s
                    WHERE id_inspeccion_cf = %s
                """
                valores = (
                    data_form['placa_vehiculo'].strip().upper(),
                    data_form['puerta_estado'],
                    data_form['puerta_facilidad'],
                    data_form['clave_precisa'],
                    data_form['clave_autorizada'],
                    data_form['perilla_funciona'],
                    data_form['numeros_visibles'],
                    data_form['caja_anclada'],
                    data_form.get('observaciones', ''),
                    id_inspeccion_cf
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                
                return {'success': True, 'message': 'Inspección actualizada correctamente'}

    except Exception as e:
        print(f"Error en actualizar_inspeccion_bd: {str(e)}")
        return {'success': False, 'message': f'Error al actualizar: {str(e)}'}
