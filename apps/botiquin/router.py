from conexion.conexionBD import conexiondb
from apps.botiquin.services import procesar_form_inspeccion_botiquin, sql_lista_inspeccionesBD, buscarInspeccionBD, buscarInspeccionBD, procesar_actualizacion_inspeccion,eliminarInspeccion
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/botiquin', tags=['botiquin'])

@router.post("/procesar_form_inspeccion_botiquin")
async def procesar_form_inspeccion_botiquin_endpoint(data: dict):
    """
    Procesa el formulario de inspección del botiquín.
    """
    try:
        resultado = procesar_form_inspeccion_botiquin(data)
        return {"success": True, "data": resultado}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/sql_lista_inspeccionesBD")
async def sql_lista_inspeccionesBD():
    """
    Obtiene la lista de inspecciones desde la base de datos.
    """
    try:
        conexion = conexiondb()
        query = "SELECT * FROM inspeccion_carretillas"
        inspecciones = conexion.execute(query).fetchall()
        return {"success": True, "data": [dict(row) for row in inspecciones]}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/buscarInspeccionBD    /{id_inspeccion}") 
async def buscar_inspeccion_bd(id_inspeccion: int):
    """
    Busca una inspección específica en la base de datos por su ID.
    """
    try:
        conexion = conexiondb()
        query = "SELECT * FROM inspecciones WHERE id = :id_inspeccion"
        inspeccion = conexion.execute(query, {"id_inspeccion": id_inspeccion}).fetchone()
        if inspeccion:
            return {"success": True, "data": dict(inspeccion)}
        else:
            return {"success": False, "error": "Inspección no encontrada"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/buscarInspeccionBD/{id_inspeccion}")
async def buscar_inspeccion_bd_v2(id_inspeccion: int):
    """
    Busca una inspección específica en la base de datos por su ID (versión alternativa).
    """
    try:
        conexion = conexiondb()
        query = "SELECT * FROM inspecciones WHERE id = :id_inspeccion"
        inspeccion = conexion.execute(query, {"id_inspeccion": id_inspeccion}).fetchone()
        if inspeccion:
            return {"success": True, "data": dict(inspeccion)}
        else:
            return {"success": False, "error": "Inspección no encontrada"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/procesar_actualizacion_inspeccion")
async def procesar_actualizacion_inspeccion(id_inspeccion: int, data: dict):
    """
    Procesa la actualización de una inspección específica en la base de datos.
    """
    try:
        conexion = conexiondb()
        query = """
        UPDATE inspecciones
        SET campo1 = :campo1, campo2 = :campo2
        WHERE id = :id_inspeccion
        """
        conexion.execute(query, {**data, "id_inspeccion": id_inspeccion})
        conexion.commit()
        return {"success": True, "message": "Inspección actualizada correctamente"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.delete("/eliminarInspeccion /{id_inspeccion}")
async def eliminar_inspeccion(id_inspeccion: int):
    """
    Elimina una inspección específica de la base de datos por su ID.
    """
    try:
        conexion = conexiondb()
        query = "DELETE FROM inspecciones WHERE id = :id_inspeccion"
        conexion.execute(query, {"id_inspeccion": id_inspeccion})
        conexion.commit()
        return {"success": True, "message": "Inspección eliminada correctamente"}
    except Exception as e:
        return {"success": False, "error": str(e)}

