import csv

import requests

from .models import Candle
from .sources.binance import BASE_URL


def fetch_history(symbol: str, interval: str, total: int = 5000) -> list[Candle]:
    """Baixa ate `total` candles recentes da Binance (1000 por requisicao)."""
    out: list[Candle] = []
    end_time = None
    while len(out) < total:
        params = {"symbol": symbol, "interval": interval, "limit": min(1000, total - len(out))}
        if end_time:
            params["endTime"] = end_time
        resp = requests.get(f"{BASE_URL}/api/v3/klines", params=params, timeout=15)
        resp.raise_for_status()
        rows = resp.json()
        if not rows:
            break
        out = [Candle(int(k[0]), *map(float, k[1:6])) for k in rows] + out
        end_time = int(rows[0][0]) - 1
    return out


def load_csv(path: str) -> list[Candle]:
    """CSV com colunas: open_time,open,high,low,close,volume (com ou sem cabecalho)."""
    with open(path, newline="") as f:
        rows = [r for r in csv.reader(f) if r and r[0].strip().lstrip("-").isdigit()]
    return [Candle(int(r[0]), *map(float, r[1:6])) for r in rows]
