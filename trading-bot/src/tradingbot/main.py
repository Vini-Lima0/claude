"""Monitor de alertas (somente avisa; nao envia ordens)."""
import time

from .config import load_config
from .notifier import Notifier, format_signal
from .risk import RiskGuard, position_size
from .sources.binance import fetch_candles
from .strategy import evaluate

POLL_SECONDS = 30


def run_once(cfg, guard, notifier, last_seen: dict[str, int]) -> None:
    for symbol in cfg.symbols:
        candles = fetch_candles(symbol, cfg.interval)
        closed = candles[:-1]  # ignora o candle ainda em formacao
        if not closed or last_seen.get(symbol) == closed[-1].open_time:
            continue
        last_seen[symbol] = closed[-1].open_time
        signal = evaluate(symbol, closed)
        if not signal:
            continue
        ok, why = guard.allows(signal)
        if not ok:
            print(f"[{symbol}] sinal bloqueado: {why}")
            continue
        qty = position_size(cfg.capital, cfg.risk_per_trade_pct, signal.entry, signal.stop)
        notifier.send(format_signal(signal, qty))
        guard.register_alert()


def main() -> None:
    cfg = load_config()
    guard = RiskGuard(cfg.capital, cfg.max_daily_loss_pct, cfg.max_alerts_per_day)
    notifier = Notifier(cfg.telegram_token, cfg.telegram_chat_id)
    last_seen: dict[str, int] = {}
    print(f"Monitorando {cfg.symbols} em {cfg.interval} (modo: somente alertas)")
    while True:
        try:
            run_once(cfg, guard, notifier, last_seen)
        except Exception as exc:  # rede instavel nao deve derrubar o monitor
            print(f"erro: {exc}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
