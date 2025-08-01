from fastapi import APIRouter, FastAPI
from apps.auth.router import auth
from apps.user.router import router as users_router
from apps.product.routes import router as products_router
from apps.employees.router import router as employees_router
from apps.usersSQL.router import router as usersSQl_router
from apps.drivers.router import router as conductores_router
from apps.vehicles.router import router as vehicles_router
from fastapi.middleware.cors import CORSMiddleware
from apps.safe.router import router as safe_router
from apps.cashless.router import router as cashless_router  # Importar el router

# Crear la aplicación FastAPI
app = FastAPI()

# Configurar CORS
origins = [
    '*',  # Origen del frontend
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

# Registrar rutas para listar empleados
app.include_router(employees_router)

# Registrar rutas para listar usuariosSQL
app.include_router(usersSQl_router)


# Registrar rutas para listar usuariosSQL
app.include_router(conductores_router)

# Registrar rutas para listar vehículos
app.include_router(vehicles_router)

app.include_router(safe_router)

# Registrar rutas para cashless
app.include_router(cashless_router)

