"""Uso: python -m tradingbot.backtest_cli BTCUSDT 5m [--csv arquivo.csv] [--n 5000]"""
import argparse

from . import backtest
from .history import fetch_history, load_csv


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("symbol")
    p.add_argument("interval")
    p.add_argument("--csv")
    p.add_argument("--n", type=int, default=5000)
    p.add_argument("--capital", type=float, default=1000)
    p.add_argument("--risk", type=float, default=0.5)
    a = p.parse_args()
    candles = load_csv(a.csv) if a.csv else fetch_history(a.symbol, a.interval, a.n)
    print(f"{len(candles)} candles")
    print(backtest.run(a.symbol, candles, a.capital, a.risk).summary())


if __name__ == "__main__":
    main()
