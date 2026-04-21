from pydantic import BaseModel
from typing import List, Dict

class Crypto(BaseModel):
    id: str
    nombre: str
    simbolo: str
    precio: float

class CryptoDetail(BaseModel):
    nombre: str
    simbolo: str
    precio_actual: float
    market_cap: float
    ranking: int

class CryptoTop(BaseModel):
    nombre: str
    precio: float

class Volatility(BaseModel):
    nombre: str
    cambio_24h: float

class ConversionResult(BaseModel):
    coin_id: str
    cantidad: float
    moneda_destino: str
    resultado: float

class HistoryPoint(BaseModel):
    timestamp: int
    precio: float

class CryptoHistory(BaseModel):
    coin_id: str
    precios: List[List[float]] # [timestamp, precio]

class AlertRequest(BaseModel):
    email: str
    coin_id: str
    target_price: float
