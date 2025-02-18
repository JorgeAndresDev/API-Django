from typing import List
from providers.firebase import products_collection  # Importa la colección de productos
from fastapi.encoders import jsonable_encoder

def get_all_products() -> List[dict]:
    try:
        # Obtener todos los documentos de la colección de productos
        products = products_collection.stream()
        
        # Convertir los documentos a un formato JSON-serializable
        product_list = []
        for doc in products:
            product = doc.to_dict()
            product['id'] = doc.id
            product_list.append(product)
        
        return product_list
    except Exception as e:
        raise e  # Maneja el error según sea necesario