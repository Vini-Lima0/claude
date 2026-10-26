"""Estrategias candidatas (long-only, adequadas a spot). Todas: f(symbol, candles) -> Signal | None.

Nenhuma tem lucratividade garantida. So considere uma estrategia valida se ela passar no
periodo fora da amostra (--split) e continuar positiva com taxas realistas.
"""
from .indicators import atr, ema
from .models import Candle, Signal
from .strategy import evaluate as ema_cross

ATR_STOP = 2.0


def rsi(closes: list[float], period: int = 14) -> float:
    if len(closes) <= period:
        return 50.0
    gains = losses = 0.0
    for a, b in zip(closes[-period - 1:-1], closes[-period:]):
        d = b - a
        gains += max(d, 0)
        losses += max(-d, 0)
    if losses == 0:
        return 100.0
    return 100 - 100 / (1 + gains / losses)


def donchian_breakout(symbol: str, candles: list[Candle], lookback: int = 20,
                      trend: int = 100, rr: float = 3.0) -> Signal | None:
    """Rompimento da maxima dos ultimos `lookback` candles, so a favor da tendencia (close > EMA)."""
    if len(candles) < max(trend, lookback) + 2:
        return None
    closes = [c.close for c in candles]
    prior_high = max(c.high for c in candles[-lookback - 1:-1])
    prev_close, close = closes[-2], closes[-1]
    if not (close > prior_high and prev_close <= prior_high and close > ema(closes, trend)[-1]):
        return None
    dist = atr(candles) * ATR_STOP
    if dist <= 0:
        return None
    return Signal(symbol, "BUY", close, close - dist, close + dist * rr,
                  f"rompeu maxima de {lookback} candles a favor da tendencia (EMA{trend})")


def trend_pullback(symbol: str, candles: list[Candle], trend: int = 100,
                   rsi_max: float = 30.0, rr: float = 1.5) -> Signal | None:
    """Compra queda (RSI baixo) dentro de tendencia de alta (close > EMA longa)."""
    if len(candles) < trend + 2:
        return None
    closes = [c.close for c in candles]
    if not (closes[-1] > ema(closes, trend)[-1]):
        return None
    if not (rsi(closes[:-1]) >= rsi_max > rsi(closes)):  # RSI acabou de cair abaixo do limite
        return None
    dist = atr(candles) * ATR_STOP
    if dist <= 0:
        return None
    close = closes[-1]
    return Signal(symbol, "BUY", close, close - dist, close + dist * rr,
                  f"RSI<{rsi_max:.0f} em tendencia de alta (EMA{trend})")


REGISTRY = {
    "ema_cross": ema_cross,
    "donchian": donchian_breakout,
    "pullback": trend_pullback,
}
