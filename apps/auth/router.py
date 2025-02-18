from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException,  Response, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from apps.auth.services import authenticate_user_services, get_user_service
from providers.auth import Token, create_access_token, create_refresh_token, get_current_user

auth = APIRouter(prefix = '/auth')

@auth.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Verificamos el token con Firebase
    user = authenticate_user_services(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    access_token = create_access_token({"sub": str(user['id'])})
    refresh_token = create_refresh_token({"sub": str(user['id'])})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@auth.get('/get_user')
async def get_user(user_id=Depends(get_current_user)):
    user = get_user_service(user_id)
    return user

@auth.get("/logout/")
def logout(response: Response):
    # Eliminar la cookie de acceso
    response.delete_cookie("access_token")
    return {'success': True, "message": "Logout exitoso"}







