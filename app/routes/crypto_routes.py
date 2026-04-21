from fastapi import APIRouter, HTTPException
from typing import List
import smtplib
from email.mime.text import MIMEText

from app.models.crypto import (
    Crypto, CryptoDetail, CryptoTop, 
    ConversionResult, CryptoHistory, AlertRequest
)
from app.services.coingecko_service import (
    get_cryptos, get_crypto_detail, 
    convert_currency, get_market_chart
)
from app.settings import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

router = APIRouter()

@router.get("/crypto") # Quitamos el response_model temporalmente para añadir el campo extra
async def list_cryptos():
    response = await get_cryptos()
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al obtener datos")
    
    data = response.json()
    return [
        {
            "id": coin["id"], 
            "nombre": coin["name"], 
            "simbolo": coin["symbol"], 
            "precio": coin["current_price"],
            "cambio_24h": coin.get("price_change_percentage_24h", 0)
        }
        for coin in data
    ]

@router.get("/crypto/{coin_id}", response_model=CryptoDetail)
async def crypto_detail(coin_id: str):
    response = await get_crypto_detail(coin_id)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Criptomoneda no encontrada")
    
    data = response.json()
    return {
        "nombre": data["name"],
        "simbolo": data["symbol"],
        "precio_actual": data["market_data"]["current_price"]["usd"],
        "market_cap": data["market_data"]["market_cap"]["usd"],
        "ranking": data["market_cap_rank"]
    }

@router.get("/convert", response_model=ConversionResult)
async def convert(coin_id: str, amount: float, target_currency: str = "usd"):
    response = await convert_currency(coin_id, amount, target_currency)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error en la conversión")
    
    data = response.json()
    if coin_id not in data:
        raise HTTPException(status_code=404, detail="Moneda no encontrada")
    
    rate = data[coin_id][target_currency]
    return {
        "coin_id": coin_id,
        "cantidad": amount,
        "moneda_destino": target_currency,
        "resultado": amount * rate
    }

@router.get("/history/{coin_id}", response_model=CryptoHistory)
async def history(coin_id: str, days: int = 7):
    response = await get_market_chart(coin_id, days)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al obtener el historial")
    
    data = response.json()
    return {
        "coin_id": coin_id,
        "precios": data["prices"]
    }

@router.post("/alert")
async def create_alert(alert: AlertRequest):
    # En un caso real, esto se guardaría en DB y un worker enviaría el mail
    # Aquí simulamos el éxito del registro
    return {"message": f"Alerta creada para {alert.coin_id} a {alert.target_price}. Se notificará a {alert.email}"}

@router.get("/report/top", response_model=List[CryptoTop])
async def top_cryptos():
    response = await get_cryptos(per_page=50)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al obtener datos")
    
    data = response.json()
    sorted_data = sorted(data, key=lambda x: x["current_price"], reverse=True)
    return [{"nombre": coin["name"], "precio": coin["current_price"]} for coin in sorted_data[:5]]

@router.get("/report/volatility")
async def volatility():
    response = await get_cryptos(per_page=20)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al obtener datos")
    
    data = response.json()
    high, low = [], []
    for coin in data:
        change = coin.get("price_change_percentage_24h")
        if change is not None:
            item = {"nombre": coin["name"], "cambio_24h": change}
            if abs(change) > 5: high.append(item)
            else: low.append(item)
    return {"alta_volatilidad": high, "baja_volatilidad": low}
