from fastapi import APIRouter, HTTPException
from .services import get_all_products, update_product, delete_product, create_product
from .schemas import ProductSchema, ProductUpdateSchema, ProductCreateSchema
from typing import List

# Crear un router para los endpoints de productos
router = APIRouter(prefix="/products", tags=["products"])

# Endpoint para obtener todos los productos
@router.get("/get_all_products")
async def get_products():
    try:
        # Obtener todos los productos desde el servicio
        products = get_all_products()
        return products
    except Exception as e:
        # Manejar errores y devolver una respuesta de error 500
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para crear un nuevo producto
@router.post("/", response_model=ProductSchema)
async def create_product_endpoint(product_data: ProductCreateSchema):
    try:
        # Convertir el objeto Pydantic a un diccionario
        product_dict = product_data.dict()
        
        # Llamar a la función create_product con await
        new_product = await create_product(product_dict)
        
        # Devolver el nuevo producto creado
        return new_product
    except Exception as e:
        # Manejar errores y devolver una respuesta de error 500
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar un producto
@router.put("/{product_id}", response_model=ProductSchema)
async def update_product_endpoint(
    product_id: str,  # ID del producto a actualizar
    product_data: ProductUpdateSchema  # Datos de actualización
):
    try:
        # Llamar a la función update_product con await
        updated_product = await update_product(product_id, product_data)
        
        # Si el producto no existe, devolver un error 404
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Devolver el producto actualizado
        return updated_product
    except Exception as e:
        # Manejar errores y devolver una respuesta de error 500
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar un producto
@router.delete("/{product_id}")
async def delete_product_endpoint(product_id: str):  # ID del producto a eliminar
    try:
        # Llamar a la función delete_product con await
        deleted = await delete_product(product_id)
        
        # Si el producto no existe, devolver un error 404
        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Devolver un mensaje de éxito
        return {"message": "Product deleted successfully"}
    except Exception as e:
        # Manejar errores y devolver una respuesta de error 500
        raise HTTPException(status_code=500, detail=str(e))