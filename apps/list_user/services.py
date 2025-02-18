from typing import List
from providers.firebase import user_collection
from fastapi.encoders import jsonable_encoder

def get_all_users() -> List[dict]:
    try:
        # Obtener todos los documentos de la colección de usuarios
        users = user_collection.stream()
        
        # Convertir los documentos a un formato JSON-serializable
        user_list = []
        for doc in users:
            user = doc.to_dict()
            user['id'] = doc.id
            user_list.append(user)
        
        return user_list
    except Exception as e:
        raise e  # Maneja el error según sea necesario