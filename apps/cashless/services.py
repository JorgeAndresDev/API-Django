from io import BytesIO
from fastapi import  HTTPException, UploadFile
import pandas as pd
from apps.cashless.schemas import UpdateCashlessSchema
from conexion.conexionBD import conexiondb


# apps/cashless/service.py
def get_all_cashless_service():
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                querySQL = """
                                SELECT 
                                    CODIGO AS codigo_cliente,
                                    CLIENTE AS cliente_nombre,
                                    DT AS Documento_pedido,
                                    PLACA AS placa_vehiculo,
                                    NUMERO AS numero_cliente,
                                    NOVEDAD AS Novedad
                                FROM tbl_cashless
                            """
                cursor.execute(querySQL)                 
                app_empresa_bd = cursor.fetchall()  # Esto ya devuelve un array
                
                # AGREGAR ESTE PRINT PARA DEBUGGING
                print(f"Tipo de datos: {type(app_empresa_bd)}")
                print(f"Cantidad de registros: {len(app_empresa_bd) if app_empresa_bd else 0}")
                
                return app_empresa_bd  # Devolver directamente, no envolver en array
        else:             
            return []  # Devolver array vacío en lugar de None
    except Exception as e:         
        print(f"Error en la función get_all_cashless: {e}")         
        return []  # Devolver array vacío en lugar de None
    finally:         
        if connection:             
            connection.close()

async def upload_cashless_service(file: UploadFile):
    try:
        contents = await file.read()
        
        try:
            df = pd.read_excel(BytesIO(contents), sheet_name='Hoja2') #en esta parte del codigo espedificamos la hoja que queremos leer
            
        except Exception as e:
            return {"error": f"Error al leer el archivo Excel: {str(e)}"}

        if df.empty:
            return {"error": "El archivo está vacío"}

        # Limpiar y verificar columnas
        df.columns = df.columns.str.strip().str.upper()
        
        print("Columnas encontradas:", df.columns.tolist())  # Debug
        
        # Verificar columnas requeridas
        required_columns = ['CODIGO', 'CLIENTE', 'DT', 'PLACA', 'NUMERO', 'NOVEDAD']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return {"error": f"Columnas faltantes en el archivo: {missing_columns}"}

        # Convertir tipos de datos con manejo de errores
        try:
            df['CODIGO'] = pd.to_numeric(df['CODIGO'], errors='coerce').fillna(0).astype(int)
            df['DT'] = pd.to_numeric(df['DT'], errors='coerce').fillna(0).astype(int)
            df['NUMERO'] = pd.to_numeric(df['NUMERO'], errors='coerce').fillna(0).astype(int)
            df['CLIENTE'] = df['CLIENTE'].astype(str)
            df['PLACA'] = df['PLACA'].astype(str)
            df['NOVEDAD'] = df['NOVEDAD'].astype(str)
        except Exception as e:
            return {"error": f"Error al convertir tipos de datos: {str(e)}"}

        # Eliminar filas con CODIGO inválido (0)
        df = df[df['CODIGO'] != 0]

        conn = conexiondb()
        if not conn:
            return {"error": "No se pudo conectar a la base de datos"}
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            for _, row in df.iterrows():
                try:
                    # Verificar si el registro existe
                    cursor.execute("SELECT 1 FROM tbl_cashless WHERE CODIGO = %s", (row['CODIGO'],))
                    exists = cursor.fetchone() is not None
                    
                    if exists:
                        query = """
                            UPDATE tbl_cashless 
                            SET CLIENTE = %s, DT = %s, PLACA = %s, NUMERO = %s, NOVEDAD = %s
                            WHERE CODIGO = %s
                        """
                    else:
                        query = """
                            INSERT INTO tbl_cashless 
                            (CODIGO, CLIENTE, DT, PLACA, NUMERO, NOVEDAD)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """
                    
                    params = (
                        row['CLIENTE'], row['DT'], row['PLACA'], 
                        row['NUMERO'], row['NOVEDAD'], row['CODIGO']
                    ) if exists else (
                        row['CODIGO'], row['CLIENTE'], row['DT'], 
                        row['PLACA'], row['NUMERO'], row['NOVEDAD']
                    )
                    
                    cursor.execute(query, params)
                    
                except Exception as row_error:
                    print(f"Error en fila CODIGO={row.get('CODIGO')}: {str(row_error)}")
                    continue
            
            conn.commit()
            return {"success": True, "message": f"Datos cargados: {len(df)} registros procesados"}
            
        except Exception as db_error:
            conn.rollback()
            return {"error": f"Error en base de datos: {str(db_error)}"}
            
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}

def update_cashless_service(cashless: UpdateCashlessSchema):
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute ( 
                    "UPDATE tbl_cashless SET NOVEDAD = %s WHERE CODIGO = %s"
                , ( cashless.NOVEDAD, cashless.CODIGO))
                connection.commit()
                return {"success": True, "message": "Registro actualizado correctamente"}
        else:
            return {"error": "No se pudo conectar a la base de datos"}
    except Exception as e:
        print(f"Error en la función update_cashless: {e}")
        return {"error": str(e)}
    finally:
        if connection:
            connection.close()

def delete_cashless_services(codigo_cliente: int):
    try:
        conexion = conexiondb()
        if not conexion:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cursor = conexion.cursor()
        query = "DELETE FROM tbl_cashless WHERE CODIGO = %s"
        cursor.execute(query, (codigo_cliente,))
        conexion.commit()
        cursor.close()
        conexion.close()

        return {"mensaje": "Cliente eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
     