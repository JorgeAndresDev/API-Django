from fastapi import APIRouter, File, HTTPException, Path, UploadFile
from fastapi.responses import JSONResponse
from flask import jsonify, request
import pandas as pd

from apps.employees.services import upload_file_service
from conexion.conexionBD import connectiondb

from .services import get_all_users, update_user, delete_user, create_user
from .schemas import UserSchema, UserUpdateSchema, UserCreateSchema
from typing import List


router = APIRouter(prefix="/users", tags=["users"])

# Endpoint para obtener todos los usuarios
@router.get("/get_all_users")
async def get_users():
    try:
        users = get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para crear un nuevo usuario
@router.post("/", response_model=UserSchema)
async def create_user(user_data: UserCreateSchema):
    try:
        new_user = create_user(user_data)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar un usuario
@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: str,
    user_data: UserUpdateSchema
):
    try:
        updated_user = update_user(user_id, user_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar un usuario
@router.delete("/{user_id}")
async def delete_user(user_id: str):
    try:
        deleted = delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
