import requests

from ..models import Candle

BASE_URL = "https://api.binance.com"  # dados publicos de mercado, sem chave


def fetch_candles(symbol: str, interval: str, limit: int = 100) -> list[Candle]:
    resp = requests.get(
        f"{BASE_URL}/api/v3/klines",
        params={"symbol": symbol, "interval": interval, "limit": limit},
        timeout=10,
    )
    resp.raise_for_status()
    return [
        Candle(int(k[0]), float(k[1]), float(k[2]), float(k[3]), float(k[4]), float(k[5]))
        for k in resp.json()
    ]
