from conexion.conexionBD import conexiondb
from apps.safe.services import procesar_form_inspeccion_caja
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix='/safe', tags=['safe'])


@router.post("/procesar_form_inspeccion_caja")  
async def procesar_form_inspeccion_caja(data: dict):
    """
    Procesa el formulario de inspección de la caja.
    """
    try:
        resultado = procesar_form_inspeccion_caja(data)
        return {"success": True, "data": resultado}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/obtener_inspecciones_cajas")
async def obtener_inspecciones_cajas():
    """
    Obtiene todas las inspecciones de cajas.
    """
    try:
        conexion = conexiondb()
        query = "SELECT * FROM inspecciones_cajas"
        inspecciones = conexion.execute(query).fetchall()
        return {"success": True, "data": [dict(row) for row in inspecciones]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/buscar_inspeccion_por_placa/{placa_vehiculo}")
async def buscar_inspeccion_por_placa(placa_vehiculo: str):
    """
    Busca inspecciones de cajas por placa de vehículo.
    """
    try:
        conexion = conexiondb()
        query = "SELECT * FROM inspecciones_cajas WHERE placa_vehiculo = :placa_vehiculo"
        inspecciones = conexion.execute(query, {"placa_vehiculo": placa_vehiculo}).fetchall()
        return {"success": True, "data": [dict(row) for row in inspecciones]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/generar_reporte_inspecciones_excel/")
async def generar_reporte_inspecciones_excel():
    """
    Genera un reporte de inspecciones de cajas en formato Excel.
    """
    try:
        # Conexión a la base de datos
        conexion = conexiondb()
        query = "SELECT * FROM inspecciones_cajas"
        inspecciones = conexion.execute(query).fetchall()

        # Convertir los resultados a un DataFrame de pandas
        df = pd.DataFrame([dict(row) for row in inspecciones])

        # Crear un archivo Excel en memoria
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Inspecciones')
        output.seek(0)

        # Devolver el archivo Excel como respuesta
        headers = {
            'Content-Disposition': 'attachment; filename="reporte_inspecciones.xlsx"'
        }
        return StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)

        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/obtener_detalle_inspeccion/") 
async def obtener_detalle_inspeccion(id_inspeccion: int):
    """
    Obtiene el detalle de una inspección específica.
    """
    try:
        conexion = conexiondb()
        query = "SELECT * FROM inspecciones_cajas WHERE id_inspeccion = :id_inspeccion"
        inspeccion = conexion.execute(query, {"id_inspeccion": id_inspeccion}).fetchone()
        if inspeccion:
            return {"success": True, "data": dict(inspeccion)}
        else:
            raise HTTPException(status_code=404, detail="Inspección no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/eliminar_inspeccion_bd/{id_inspeccion}")
async def eliminar_inspeccion_bd(id_inspeccion: int):
    """
    Elimina una inspección específica de la base de datos.
    """
    try:
        conexion = conexiondb()
        query = "DELETE FROM inspecciones_cajas WHERE id_inspeccion = :id_inspeccion"
        result = conexion.execute(query, {"id_inspeccion": id_inspeccion})
        if result.rowcount > 0:
            return {"success": True, "message": "Inspección eliminada correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Inspección no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

