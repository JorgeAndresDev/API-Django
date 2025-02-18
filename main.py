from fastapi import FastAPI
from apps.auth.router import auth
from apps.list_user.routes import router as list_users_router
from apps.list_product.routes import router as products_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Registrar rutas de autenticación
app.include_router(auth)

# Registrar rutas para listar usuarios
app.include_router(list_users_router)

# Registrar rutas para listar productos
app.include_router(products_router)