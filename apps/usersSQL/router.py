
from fastapi import APIRouter, HTTPException
from apps.usersSQL.services import get_all_users_service
from apps.usersSQL.schemas import UserCreateSchema, UserUpdateSchema
from apps.usersSQL.services import create_user_service, update_user_service, delete_user_service


router = APIRouter(prefix="/usersSQL", tags=["usersSQL"])

@router.get("/get_all_users")
async def get_all_users():
    try:
        users = get_all_users_service()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/create_user")
async def create_user(user: UserCreateSchema):
    try:
        response = create_user_service(user)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update_user")
async def update_user(user: UserUpdateSchema):
    try:
        response = update_user_service(user)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/delete_user/{userId}")
async def delete_user(userId: int):
    try:
        response = delete_user_service(userId)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))