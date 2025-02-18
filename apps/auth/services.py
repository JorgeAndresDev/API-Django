from providers.firebase import user_collection
from fastapi.encoders import jsonable_encoder
from firebase_admin import firestore

def authenticate_user_services(username: str, password: str):

    user = user_collection.where(u'user', u'==', username).where(u'password', u'==', password).stream()
    
    for doc in user:
        user = doc.to_dict()
        user['id'] = doc.id
        break

    if user is None or 'password' not in user:
        return False

    hashed_password = user.get('password')
    if hashed_password is None:
        return False
    
    
    return user

def get_user_service(user_id):

    user_doc = user_collection.document(user_id).get()
    
    if not user_doc.exists:
        return None  

    user = user_doc.to_dict()
    user['id'] = user_doc.id

    # Asegúrate de que el resultado sea JSON-serializable
    user = jsonable_encoder(user)

    return user

def create_user_service(user_data: dict):

    user = user_collection.add(user_data)
    user_data['id'] = user[1].id

    return user_data
