from fastapi import APIRouter, HTTPException
from .services import get_all_users
from .schemas import UserSchema
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.get(
    "/",
    response_model=List[UserSchema],
    summary="Listar todos los usuarios",
    description="Obtiene una lista de todos los usuarios registrados en la base de datos.",
    responses={
        200: {
            "description": "Lista de usuarios obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "12345",
                            "user": "johndoe",
                            "password": "4321",
                        },
                    ]
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Error al obtener los usuarios"}
                }
            }
        }
    }
)
async def list_users():
    try:
        users = get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))