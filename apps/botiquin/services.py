# import os
# import datetime
# import openpyxl
# from flask import send_file

# from conexion.conexionBD import conexiondb

# def procesar_form_inspeccion_caja(dataForm):
#     try:
#         # Validación de campos requeridos
#         campos_requeridos = [
#             'placa_vehiculo', 'puerta_estado', 'puerta_facilidad',
#             'clave_precisa', 'clave_autorizada', 'perilla_funciona',
#             'numeros_visibles', 'caja_anclada'
#         ]
        
#         for campo in campos_requeridos:
#             if campo not in dataForm or not dataForm[campo]:
#                 raise ValueError(f"El campo {campo} es requerido")

#         with conexiondb() as conexion_MySQLdb:
#             with conexion_MySQLdb.cursor(dictionary=True) as cursor:
#                 sql = """INSERT INTO inspeccion_cajas_fuertes 
#                         (placa_vehiculo, puerta_estado, puerta_facilidad, clave_precisa, 
#                          clave_autorizada, perilla_funciona, numeros_visibles, 
#                          caja_anclada, observaciones) 
#                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

#                 # Manejo de observaciones (puede ser NULL)
#                 observaciones = dataForm['observaciones'] if 'observaciones' in dataForm and dataForm['observaciones'] else None

#                 valores = (
#                     dataForm['placa_vehiculo'].strip().upper(),  # Normalización de placa
#                     dataForm['puerta_estado'],
#                     dataForm['puerta_facilidad'],
#                     dataForm['clave_precisa'],
#                     dataForm['clave_autorizada'],
#                     dataForm['perilla_funciona'],
#                     dataForm['numeros_visibles'],
#                     dataForm['caja_anclada'],
#                     observaciones  # Manejo de NULL
#                 )
                
#                 cursor.execute(sql, valores)
#                 conexion_MySQLdb.commit()
                
#                 if cursor.rowcount == 1:
#                     return cursor.lastrowid  # Retorna el ID insertado
#                 return None

#     except Exception as e:
#         print(f"Error en procesar_form_inspeccion_caja: {str(e)}")
#         if 'conexion_MySQLdb' in locals():
#             conexion_MySQLdb.rollback()
#         return None
    


# def sql_lista_inspeccionesBD():
#     try:
#         with conexiondb() as conexion_MySQLdb:
#             with conexion_MySQLdb.cursor(dictionary=True) as cursor:
#                 querySQL = """
#                     SELECT 
#                         id_inspeccion,
#                         placa_vehiculo,
#                         puerta_estado,
#                         puerta_facilidad,
#                         clave_precisa,
#                         clave_autorizada,
#                         perilla_funciona,
#                         numeros_visibles,
#                         caja_anclada,
#                         observaciones,
#                         DATE_FORMAT(fecha_inspeccion, '%Y-%m-%d %H:%i') AS fecha_inspeccion_formateada
#                     FROM inspeccion_cajas_fuertes
#                     ORDER BY fecha_inspeccion DESC
#                 """
#                 cursor.execute(querySQL)
#                 return cursor.fetchall()
#     except Exception as e:
#         print(f"Error en obtener_inspecciones_cajas: {str(e)}")
#         return None


# def buscar_inspeccion_por_placa(placa):
#     try:
#         with conexiondb() as conexion_MySQLdb:
#             with conexion_MySQLdb.cursor(dictionary=True) as cursor:
#                 querySQL = """
#                     SELECT * FROM inspeccion_cajas_fuertes 
#                     WHERE placa_vehiculo LIKE %s
#                     ORDER BY fecha_inspeccion DESC
#                 """
#                 cursor.execute(querySQL, (f"%{placa}%",))
#                 return cursor.fetchall()
#     except Exception as e:
#         print(f"Error en buscar_inspeccion_por_placa: {str(e)}")
#         return None


# def generar_reporte_inspecciones_excel():
#     try:
#         inspecciones = obtener_inspecciones_cajas()
#         if not inspecciones:
#             return None

#         wb = openpyxl.Workbook()
#         hoja = wb.active
#         hoja.title = "Inspecciones Cajas Fuertes"

#         # Encabezados
#         cabeceras = [
#             "ID", "Placa Vehículo", "Puerta Estado", "Puerta Facilidad", 
#             "Clave Precisa", "Clave Autorizada", "Perilla Funciona",
#             "Números Visibles", "Caja Anclada", "Observaciones", "Fecha Inspección"
#         ]
#         hoja.append(cabeceras)

#         # Datos
#         for inspeccion in inspecciones:
#             fila = [
#                 inspeccion['id_inspeccion'],
#                 inspeccion['placa_vehiculo'],
#                 inspeccion['puerta_estado'],
#                 inspeccion['puerta_facilidad'],
#                 inspeccion['clave_precisa'],
#                 inspeccion['clave_autorizada'],
#                 inspeccion['perilla_funciona'],
#                 inspeccion['numeros_visibles'],
#                 inspeccion['caja_anclada'],
#                 inspeccion['observaciones'],
#                 inspeccion['fecha_inspeccion_formateada']
#             ]
#             hoja.append(fila)

#         # Guardar archivo
#         fecha_actual = datetime.datetime.now().strftime('%Y_%m_%d')
#         nombre_archivo = f"Reporte_Inspecciones_{fecha_actual}.xlsx"
#         carpeta_descarga = "../static/downloads-excel"
#         ruta_descarga = os.path.join(os.path.dirname(__file__), carpeta_descarga)

#         if not os.path.exists(ruta_descarga):
#             os.makedirs(ruta_descarga)
#             os.chmod(ruta_descarga, 0o755)

#         ruta_completa = os.path.join(ruta_descarga, nombre_archivo)
#         wb.save(ruta_completa)

#         return send_file(ruta_completa, as_attachment=True)

#     except Exception as e:
#         print(f"Error en generar_reporte_inspecciones_excel: {str(e)}")
#         return None
    
    
# def obtener_detalle_inspeccion(id_inspeccion):
#     try:
#         with conexiondb() as conexion_MySQLdb:
#             with conexion_MySQLdb.cursor(dictionary=True) as cursor:
#                 querySQL = """
#                     SELECT 
#                         id_inspeccion,
#                         placa_vehiculo,
#                         puerta_estado,
#                         puerta_facilidad,
#                         clave_precisa,
#                         clave_autorizada,
#                         perilla_funciona,
#                         numeros_visibles,
#                         caja_anclada,
#                         observaciones,
#                         IFNULL(DATE_FORMAT(fecha_inspeccion, '%d/%m/%Y %H:%i'), 'No registrada') AS fecha_inspeccion_formateada,
#                         fecha_inspeccion
#                     FROM inspeccion_cajas_fuertes
#                     WHERE id_inspeccion = %s
#                 """
#                 cursor.execute(querySQL, (id_inspeccion,))
#                 return cursor.fetchone()
#     except Exception as e:
#         print(f"Error en obtener_detalle_inspeccion: {str(e)}")
#         return None
    
# # Función para eliminar inspección
# def eliminar_inspeccion_bd(id_inspeccion):
#     try:
#         with conexiondb() as conexion_MySQLdb:
#             with conexion_MySQLdb.cursor(dictionary=True) as cursor:
#                 # Verificar si existe la inspección
#                 cursor.execute("SELECT id_inspeccion FROM inspeccion_cajas_fuertes WHERE id_inspeccion = %s", (id_inspeccion,))
#                 if not cursor.fetchone():
#                     return {'success': False, 'message': 'La inspección no existe'}

#                 # Eliminar la inspección
#                 cursor.execute("DELETE FROM inspeccion_cajas_fuertes WHERE id_inspeccion = %s", (id_inspeccion,))
#                 conexion_MySQLdb.commit()
#                 return {'success': True, 'message': 'Inspección eliminada correctamente'}

#     except Exception as e:
#         print(f"Error en eliminar_inspeccion_bd: {str(e)}")
#         return {'success': False, 'message': f'Error al eliminar: {str(e)}'}

# # Función para actualizar inspección
# def actualizar_inspeccion_bd(id_inspeccion, data_form):
#     try:
#         campos_requeridos = [
#             'placa_vehiculo', 'puerta_estado', 'puerta_facilidad',
#             'clave_precisa', 'clave_autorizada', 'perilla_funciona',
#             'numeros_visibles', 'caja_anclada'
#         ]
        
#         # Validar campos requeridos
#         for campo in campos_requeridos:
#             if campo not in data_form or not data_form[campo]:
#                 return {'success': False, 'message': f'El campo {campo} es requerido'}

#         with conexiondb() as conexion_MySQLdb:
#             with conexion_MySQLdb.cursor(dictionary=True) as cursor:
#                 sql = """
#                     UPDATE inspeccion_cajas_fuertes 
#                     SET 
#                         placa_vehiculo = %s,
#                         puerta_estado = %s,
#                         puerta_facilidad = %s,
#                         clave_precisa = %s,
#                         clave_autorizada = %s,
#                         perilla_funciona = %s,
#                         numeros_visibles = %s,
#                         caja_anclada = %s,
#                         observaciones = %s
#                     WHERE id_inspeccion = %s
#                 """
#                 valores = (
#                     data_form['placa_vehiculo'].strip().upper(),
#                     data_form['puerta_estado'],
#                     data_form['puerta_facilidad'],
#                     data_form['clave_precisa'],
#                     data_form['clave_autorizada'],
#                     data_form['perilla_funciona'],
#                     data_form['numeros_visibles'],
#                     data_form['caja_anclada'],
#                     data_form.get('observaciones', ''),
#                     id_inspeccion
#                 )
#                 cursor.execute(sql, valores)
#                 conexion_MySQLdb.commit()
                
#                 return {'success': True, 'message': 'Inspección actualizada correctamente'}

#     except Exception as e:
#         print(f"Error en actualizar_inspeccion_bd: {str(e)}")
#         return {'success': False, 'message': f'Error al actualizar: {str(e)}'}
