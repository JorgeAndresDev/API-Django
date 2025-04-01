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
                    dataForm.get('observaciones', '')
                )
                
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"Error en procesar_form_inspeccion: {e}")
        return None

def sql_lista_inspeccionesBD():
    try:
        with coconexiondbnectionBD() as conexion_MySQLdb:
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
                ORDER BY id_inspeccion DESC
                """
                cursor.execute(querySQL)
                return cursor.fetchall()
    except Exception as e:
        print(f"Error en sql_lista_inspeccionesBD: {e}")
        return None

def sql_detalles_inspeccionBD(id_inspeccion):
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
                return cursor.fetchone()
    except Exception as e:
        print(f"Error en sql_detalles_inspeccionBD: {e}")
        return None

def buscarInspeccionBD(search):
    try:
        with conexiondb() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                SELECT 
                    id_inspeccion,
                    placa_vehiculo,
                    DATE_FORMAT(fecha_inspeccion, '%Y-%m-%d %H:%i') AS fecha_inspeccion
                FROM inspecciones_botiquines
                WHERE placa_vehiculo LIKE %s
                ORDER BY id_inspeccion DESC
                """
                cursor.execute(querySQL, (f"%{search}%",))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error en buscarInspeccionBD: {e}")
        return []

def buscarInspeccionBD(search):
    try:
        with conexiondb() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                SELECT 
                    id_inspeccion,
                    placa_vehiculo,
                    DATE_FORMAT(fecha_inspeccion, '%Y-%m-%d %H:%i') AS fecha_inspeccion
                FROM inspecciones_botiquines
                WHERE placa_vehiculo LIKE %s
                ORDER BY id_inspeccion DESC
                """
                cursor.execute(querySQL, (f"%{search}%",))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error en buscarInspeccionBD: {e}")
        return []


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
                    dataForm.get('observaciones', ''),
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
                return cursor.rowcount 
    except Exception as e:
        print(f"Error en eliminarInspeccion: {e}")
        return None
