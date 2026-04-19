from fastapi import APIRouter, HTTPException
from typing import List

from app.models.crypto import Crypto, CryptoDetail, CryptoTop
from app.services.coingecko_service import get_cryptos, get_crypto_detail

router = APIRouter()

@router.get("/crypto", response_model=List[Crypto])
def list_cryptos():
    response = get_cryptos()

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al obtener datos")

    data = response.json()

    return [
        {
            "id": coin["id"],
            "nombre": coin["name"],
            "simbolo": coin["symbol"],
            "precio": coin["current_price"]
        }
        for coin in data
    ]

@router.get("/crypto/{coin_id}", response_model=CryptoDetail)
def crypto_detail(coin_id: str):
    response = get_crypto_detail(coin_id)

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

@router.get("/report/top", response_model=List[CryptoTop])
def top_cryptos():
    response = get_cryptos(per_page=50)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al obtener datos")

    data = response.json()

    sorted_data = sorted(data, key=lambda x: x["current_price"], reverse=True)
    top_5 = sorted_data[:5]

    return [
        {
            "nombre": coin["name"],
            "precio": coin["current_price"]
        }
        for coin in top_5
    ]

@router.get("/report/volatility")
def volatility():
    response = get_cryptos(per_page=20)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al obtener datos")

    data = response.json()

    high_volatility = []
    low_volatility = []

    for coin in data:
        change = coin.get("price_change_percentage_24h")

        if change is not None:
            item = {
                "nombre": coin["name"],
                "cambio_24h": change
            }

            if abs(change) > 5:
                high_volatility.append(item)
            else:
                low_volatility.append(item)

    return {
        "alta_volatilidad": high_volatility,
        "baja_volatilidad": low_volatility
    }