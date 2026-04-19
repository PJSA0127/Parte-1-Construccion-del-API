from fastapi import FastAPI
from app.routes.crypto_routes import router as crypto_router

app = FastAPI(
    title="API de Criptomonedas",
    description="API para consultar datos y generar reportes de criptos",
    version="1.0.0"
)

# Registrar rutas
app.include_router(crypto_router)

@app.get("/")
def home():
    return {"message": "Bienvenido a la API de Criptomonedas"}

