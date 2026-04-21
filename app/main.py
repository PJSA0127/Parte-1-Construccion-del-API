from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.crypto_routes import router as crypto_router
from app.settings import API_TITLE, API_VERSION

app = FastAPI(
    title="Crypto Dashboard API",
    description="API avanzada para consultar datos y generar reportes de criptos",
    version=API_VERSION
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Registrar rutas
app.include_router(crypto_router)

@app.get("/")
def home():
    return {"message": "Bienvenido a Crypto Dashboard API"}
