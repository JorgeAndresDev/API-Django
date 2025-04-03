from conexion.conexionBD import conexiondb
from apps.botiquin.services import procesar_form_inspeccion_botiquin, sql_lista_inspeccionesBD, procesar_actualizacion_inspeccion,eliminarInspeccion, generar_reporte_inspecciones
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse



router = APIRouter(prefix='/botiquin', tags=['botiquin'])

@router.post("/procesar_form_inspeccion_botiquin")
async def procesar_form_inspeccion_botiquin_endpoint(data: dict):
    """
    Procesa el formulario de inspección del botiquín.
    """
    try:
        resultado = procesar_form_inspeccion_botiquin(data)
        if "error" in resultado:
            return {"success": False, "error": resultado["error"]}
        return {"success": True, "data": resultado}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/sql_lista_inspeccionesBD")
async def obtener_lista_inspecciones():
    """
    Endpoint para obtener la lista de inspecciones desde la base de datos.
    """
    try:
        resultado = sql_lista_inspeccionesBD()
        if resultado is not None and len(resultado) > 0:
            return {"success": True, "data": resultado}
        elif resultado == []:
            return {"success": False, "error": "No hay registros en inspecciones_botiquines"}
        else:
            return {"success": False, "error": "Error al ejecutar la consulta"}
    except Exception as e:
        return {"success": False, "error": str(e)}



@router.put("/procesar_actualizacion_inspeccion/{id_inspeccion}")
async def procesar_actualizacion_inspeccion_api(id_inspeccion: int, data: dict):
    """
    Procesa la actualización de una inspección específica en la base de datos.
    """
    try:
        # Llama a la función que ya está bien estructurada
        data["id_inspeccion"] = id_inspeccion  # Agrega el ID al diccionario de datos
        resultado = procesar_actualizacion_inspeccion(data)

        if resultado:
            return {"success": True, "message": "Inspección actualizada correctamente"}
        else:
            return {"success": False, "error": "No se pudo actualizar la inspección"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.delete("/eliminarInspeccion/{id_inspeccion}")
async def eliminar_inspeccion(id_inspeccion: int):
    """
    Elimina una inspección específica de la base de datos por su ID.
    """
    try:
        resultado = eliminarInspeccion(id_inspeccion)
        return resultado
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/descargar-reporte-inspecciones")
async def reporteInspeccionesExcel():
    try:
        reporte = generar_reporte_inspecciones()
        if isinstance(reporte, FileResponse):
            return reporte
        return reporte  # Devuelve el error en formato JSON
    except Exception as e:
        return {"success": False, "error": str(e)}
