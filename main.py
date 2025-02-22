from fastapi import FastAPI
from apps.auth.router import auth
from apps.user.routes import router as users_router
from apps.product.routes import router as products_router
from fastapi.middleware.cors import CORSMiddleware

# Crear la aplicación FastAPI
app = FastAPI()

# Configurar CORS
origins = [
    "http://127.0.0.1:8000",  # Origen del frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir solo el origen del frontend
    allow_credentials=True,  # Permitir credenciales (cookies, headers de autenticación)
    allow_methods=["*"],     # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],     # Permitir todos los encabezados
)

# Registrar rutas de autenticación
app.include_router(auth)

# Registrar rutas para listar usuarios
app.include_router(users_router)

# Registrar rutas para listar productos
app.include_router(products_router)