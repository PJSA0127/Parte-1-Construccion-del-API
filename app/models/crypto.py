from pydantic import BaseModel

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