
from fastapi import APIRouter, HTTPException
from apps.user.schemas import UserCreateSchema, UserUpdateSchema
from apps.user.services import get_all_users
from apps.usersSQL.services import create_users, delete_users, update_users


router = APIRouter(prefix="/usersSQL", tags=["usersSQL"])

@router.get("/get_all_users")
async def get_users():
    try:
        users = get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/create_user")
async def create_user(user: UserCreateSchema):
    try:
        user_data = user.model_dump()  # Convertir a diccionario
        response = create_users(user_data)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update_user")
async def update_user(user: UserUpdateSchema):
    try:
        response = update_users(user)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: str):
    try:
        response = delete_users(user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))