"""Estrategia de exemplo: cruzamento de EMA9/EMA21 com stop por ATR.

E apenas um ponto de partida para testar a estrutura. Nao ha evidencia de que seja lucrativa:
valide com backtest e paper trading antes de confiar em qualquer sinal.
"""
from .indicators import atr, ema
from .models import Candle, Signal

FAST, SLOW = 9, 21
ATR_STOP_MULT = 1.5
RISK_REWARD = 2.0


def evaluate(symbol: str, candles: list[Candle]) -> Signal | None:
    if len(candles) < SLOW + 2:
        return None
    closes = [c.close for c in candles]
    fast, slow = ema(closes, FAST), ema(closes, SLOW)
    crossed_up = fast[-2] <= slow[-2] and fast[-1] > slow[-1]
    crossed_down = fast[-2] >= slow[-2] and fast[-1] < slow[-1]
    if not (crossed_up or crossed_down):
        return None

    entry = closes[-1]
    dist = atr(candles) * ATR_STOP_MULT
    if dist <= 0:
        return None
    if crossed_up:
        return Signal(symbol, "BUY", entry, entry - dist, entry + dist * RISK_REWARD,
                      f"EMA{FAST} cruzou acima da EMA{SLOW}")
    return Signal(symbol, "SELL", entry, entry + dist, entry - dist * RISK_REWARD,
                  f"EMA{FAST} cruzou abaixo da EMA{SLOW}")
