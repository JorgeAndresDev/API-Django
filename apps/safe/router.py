from conexion.conexionBD import conexiondb
from apps.safe.services import procesar_form_inspeccion_caja, obtener_inspecciones_cajas, eliminar_inspeccion_cf
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
import traceback

router = APIRouter(prefix='/safe', tags=['safe'])


@router.post("/procesar_form_inspeccion_caja")  
async def endpoint_procesar_form_inspeccion_caja(data: dict):
    """
    Procesa el formulario de inspección de la caja.
    """
    try:
        resultado = procesar_form_inspeccion_caja(data)
        return {"success": True, "data": resultado}
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/obtener_inspecciones_cajas")
async def endpoint_obtener_inspecciones_cajas():
    """
    Obtiene todas las inspecciones de cajas.
    """
    try:
        conexion = conexiondb()
        cursor = conexion.cursor(dictionary=True)

        query = "SELECT * FROM inspeccion_cajas_fuertes"
        cursor.execute(query)
        inspecciones = cursor.fetchall()

        cursor.close()
        conexion.close()

        return {"success": True, "data": inspecciones}
    except Exception as e:
        print("Error en endpoint_obtener_inspecciones_cajas:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/eliminar_inspeccion_cf/{id_inspeccion_cf}")
async def endpoint_eliminar_inspeccion_cf(id_inspeccion_cf: int):
    """
    Elimina una inspección de caja fuerte por su ID.
    """
    try:
        resultado = eliminar_inspeccion_cf(id_inspeccion_cf)
        if resultado:
            return {"success": True, "message": "Inspección eliminada correctamente."}
        else:
            raise HTTPException(status_code=404, detail="Inspección no encontrada.")
    except Exception as e:
        print("Error en endpoint_eliminar_inspeccion_cf:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

