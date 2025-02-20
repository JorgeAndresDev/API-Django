from typing import List, Optional
from providers.firebase import user_collection
from fastapi.encoders import jsonable_encoder

def get_all_users() -> List[dict]:
    try:
        users = user_collection.stream()
        user_list = []
        for doc in users:
            user = doc.to_dict()
            user['id'] = doc.id
            user_list.append(user)
        return user_list
    except Exception as e:
        raise e

def create_user(user_data) -> dict:
    try:
        # Crear un nuevo documento en Firestore
        new_user_ref = user_collection.document()
        new_user_ref.set(user_data.dict())
        
        # Obtener el usuario creado
        new_user = new_user_ref.get().to_dict()
        new_user['id'] = new_user_ref.id
        return new_user
    except Exception as e:
        raise e

def update_user(user_id: str, user_data) -> Optional[dict]:
    try:
        user_ref = user_collection.document(user_id)
        user = user_ref.get()
        if not user.exists:
            return None
        update_data = user_data.dict(exclude_unset=True)
        user_ref.update(update_data)
        updated_user = user_ref.get().to_dict()
        updated_user['id'] = user_id
        return updated_user
    except Exception as e:
        raise e

def delete_user(user_id: str) -> bool:
    try:
        user_ref = user_collection.document(user_id)
        user = user_ref.get()
        if not user.exists:
            return False
        user_ref.delete()
        return True
    except Exception as e:
        raise e