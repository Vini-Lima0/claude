from dataclasses import dataclass


@dataclass(frozen=True)
class Candle:
    open_time: int  # ms epoch
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True)
class Signal:
    symbol: str
    side: str  # "BUY" ou "SELL"
    entry: float
    stop: float
    target: float
    reason: str
