import requests

BASE_URL = "https://api.coingecko.com/api/v3"


def get_cryptos(vs_currency="usd", per_page=10):
    url = f"{BASE_URL}/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": 1
    }
    return requests.get(url, params=params)


def get_crypto_detail(coin_id: str):
    url = f"{BASE_URL}/coins/{coin_id}"
    return requests.get(url)