from fastapi import FastAPI, HTTPException
from typing import List
from app.schemas.evento_schema import Evento

app = FastAPI(title="API Monitoreo SOS")

# Base de datos temporal (lista en memoria)
eventos = []


# 🔹 Ruta raíz
@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}


# 🔹 Obtener todos los eventos
@app.get("/eventos", response_model=List[dict])
def obtener_eventos():
    return eventos


# 🔹 Crear evento
@app.post("/eventos")
def crear_evento(evento: Evento):
    evento_dict = evento.dict()
    evento_dict["id"] = len(eventos) + 1
    evento_dict["estado"] = "pendiente"

    eventos.append(evento_dict)

    return {
        "mensaje": "Evento creado correctamente",
        "data": evento_dict
    }


# 🔹 Resolver evento
@app.put("/eventos/{evento_id}")
def resolver_evento(evento_id: int):
    for evento in eventos:
        if evento["id"] == evento_id:
            evento["estado"] = "resuelto"
            return {
                "mensaje": "Evento actualizado",
                "data": evento
            }

    raise HTTPException(status_code=404, detail="Evento no encontrado")