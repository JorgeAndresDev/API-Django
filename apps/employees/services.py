import datetime
from io import BytesIO
from flask import make_response
import pandas as pd
from fastapi import HTTPException, UploadFile
from apps.employees.schema import EmployeeCreateSchema, UpdateEmployeeSchema
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
                        CENTRO,
                        CASH,
                        SAC,
                        `CHECK`,
                        `MOD`,
                        ER,
                        PARADAS,
                        PERFORMANCE                                            
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

async def upload_cashless(file: UploadFile):
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



def delete_empleado_services(cc: int):
    try:
        conexion = conexiondb()
        if not conexion:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cursor = conexion.cursor()
        query = "DELETE FROM tbl_empleados WHERE cc = %s"
        cursor.execute(query, (cc,))
        conexion.commit()
        cursor.close()
        conexion.close()

        return {"mensaje": "Empleado eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def download_employees_report_service():
    try:
        # Conectar a la base de datos
        conn = conexiondb()
        cursor = conn.cursor(dictionary=True)
        
        # Consultar todos los datos de la tabla de empleados
        sql = "SELECT * FROM tbl_empleados"
        cursor.execute(sql)
        empleados = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not empleados:
            # Si no hay datos, puedes mostrar un mensaje o redirigir
            return "La base de datos esta vacia, no se puede generer un reporte :("
        
        # Crear un DataFrame con los datos
        df = pd.DataFrame(empleados)
        
        # Crear un buffer para el archivo Excel
        output = BytesIO()
        
        # Crear un writer de Excel
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        
        # Escribir el DataFrame al archivo Excel
        df.to_excel(writer, sheet_name='Empleados', index=False)
        
        # Obtener el libro de trabajo y la hoja
        workbook = writer.book
        worksheet = writer.sheets['Empleados']
        
        # Añadir formato a las columnas (opcional)
        # Por ejemplo, formato para columnas numéricas y porcentuales
        formato_porcentaje = workbook.add_format({'num_format': '0.00%'})
        formato_numero = workbook.add_format({'num_format': '0.00'})
        
        # Aplicar formato a columnas específicas (ajusta los índices según tus columnas)
        # Por ejemplo, si CHECK, MOD, ER son porcentajes:
        for col_idx, col_name in enumerate(df.columns):
            if col_name in ['CHECK', 'MOD', 'ER', 'PERFORMANCE']:
                # Convertir de texto a número si es necesario
                worksheet.set_column(col_idx, col_idx, 12, formato_porcentaje)
            elif col_name in ['CASH', 'SAC', 'PARADAS']:
                worksheet.set_column(col_idx, col_idx, 12, formato_numero)
        
        # Ajustar el ancho de las columnas automáticamente
        for i, col in enumerate(df.columns):
            column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_width)
        
        # Guardar el archivo
        writer.close()
        
        # Reiniciar el puntero del buffer al principio
        output.seek(0)
        
        # Configurar la respuesta para la descarga del archivo
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Informe_Empleados_{fecha_actual}.xlsx"
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        return response
        
    except Exception as e:
        # Manejo de errores
        return f"Error al generar el informe: {str(e)}", 500

def sql_detalles_empleadoBD(cc):
    try:
        with conexiondb() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                SELECT 
                    CC,
                    NOM,
                    CAR,
                    CENTRO,
                    CASH,
                    SAC,
                    CHECK,
                    MOD,
                    ER,
                    PARADAS,
                    PERFORMANCE
                FROM tbl_empleados
                WHERE CC = %s
                """
                cursor.execute(querySQL, (cc,))
                return cursor.fetchone()
    except Exception as e:
        print(f"Error en sql_detalles_empleadoBD: {e}")
        return None

def update_employee_service(employee: UpdateEmployeeSchema):
    try:
        conexion = conexiondb()
        cursor = conexion.cursor()
        cursor.execute(
                    "UPDATE tbl_empleados SET NOM = %s, CAR = %s, CENTRO = %s , CASH = %s, SAC = %s, `CHECK` = %s, `MOD` = %s, ER = %s, PARADAS = %s, PERFORMANCE = %s WHERE CC = %s",
                    (employee.NOM, employee.CAR, employee.CENTRO, None, None, None, None, None, None, None, employee.CC)
                )
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "Empleado actualizado exitosamente"}
        
    except Exception as e:
        print(f"Error en actualizar_empleadoBD: {e}")
        return False

def create_employee_service(employee: EmployeeCreateSchema):
    try:
        conexion = conexiondb()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO tbl_empleados (CC, NOM, CAR, CENTRO, CASH, SAC, `CHECK`, `MOD`, ER, PARADAS, PERFORMANCE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (employee.CC, employee.NOM, employee.CAR, employee.CENTRO, None, None, None, None, None, None, None)
        )
        cursor.close()
        conexion.commit()
        conexion.close()
        return {'success': True, "message": "Empleado creado correctamente"}

    except Exception as e:
        print(f" Error al crear el empleado: {e}")
    return {'success': False, "message": "Error al crear el empleado"}

    
