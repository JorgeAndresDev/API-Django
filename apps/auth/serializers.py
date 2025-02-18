from fastapi import HTTPException, status
from google.cloud.firestore_v1 import DocumentSnapshot



def user_serializer(user: DocumentSnapshot) -> dict:

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    user_dict = user.to_dict()
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Invalid user data"
        )
    
    return {
        "id": user.id,
        "user": user_dict.get("user"),
        "password": user_dict.get("password"),
    }