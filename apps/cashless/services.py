from io import BytesIO
from fastapi import FastAPI, UploadFile, File
import pandas as pd
from conexion.conexionBD import conexiondb


def get_all_cashless_service():
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                querySQL = """                     
                    SELECT                         
                        CODIGO,
                        CLIENTE,                         
                        DT,                         
                        PLACA,
                        NUMERO,
                        NOVEDAD                                                                  
                    FROM tbl_cashless                                    
                """ 
                cursor.execute(querySQL)                 
                app_empresa_bd = cursor.fetchall()                 
                return app_empresa_bd
        else:             
            return None     
    except Exception as e:         
        print(f"Error en la función get_all_cashless: {e}")         
        return None     
    finally:         
        if connection:             
            connection.close()


async def upload_file_service(file: UploadFile):
    try:
        contents = await file.read()
        
        try:
            df = pd.read_excel(BytesIO(contents), sheet_name=0)
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


     