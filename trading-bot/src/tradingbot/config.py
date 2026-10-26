import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    symbols: tuple[str, ...]
    interval: str
    capital: float
    risk_per_trade_pct: float
    max_daily_loss_pct: float
    max_alerts_per_day: int
    telegram_token: str
    telegram_chat_id: str


def load_config() -> Config:
    env = os.environ
    return Config(
        symbols=tuple(s.strip() for s in env.get("SYMBOLS", "BTCUSDT").split(",") if s.strip()),
        interval=env.get("INTERVAL", "5m"),
        capital=float(env.get("CAPITAL", "1000")),
        risk_per_trade_pct=float(env.get("RISK_PER_TRADE_PCT", "0.5")),
        max_daily_loss_pct=float(env.get("MAX_DAILY_LOSS_PCT", "2")),
        max_alerts_per_day=int(env.get("MAX_ALERTS_PER_DAY", "10")),
        telegram_token=env.get("TELEGRAM_BOT_TOKEN", ""),
        telegram_chat_id=env.get("TELEGRAM_CHAT_ID", ""),
    )
