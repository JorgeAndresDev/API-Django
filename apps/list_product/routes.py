from fastapi import APIRouter, HTTPException
from .services import get_all_products
from .schemas import ProductSchema
from typing import List

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductSchema])
async def list_products():
    try:
        products = get_all_products()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))