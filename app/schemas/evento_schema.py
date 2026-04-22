from pydantic import BaseModel

class Evento(BaseModel):
    cliente: str
    tipo_evento: str
    descripcion: str