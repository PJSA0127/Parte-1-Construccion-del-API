import httpx
from app.settings import COINGECKO_BASE_URL

async def get_cryptos(vs_currency="usd", per_page=10):
    url = f"{COINGECKO_BASE_URL}/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": 1
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        return response

async def get_crypto_detail(coin_id: str):
    url = f"{COINGECKO_BASE_URL}/coins/{coin_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response

async def convert_currency(coin_id: str, amount: float, target_currency: str):
    url = f"{COINGECKO_BASE_URL}/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": target_currency
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        return response

async def get_market_chart(coin_id: str, days: int = 7):
    url = f"{COINGECKO_BASE_URL}/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        return response
