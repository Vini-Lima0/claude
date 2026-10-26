"""Uso: python -m tradingbot.backtest_cli BTCUSDT 1h [--strategy donchian] [--n 5000] [--fee 0.1]
        [--split 0.7] [--csv arquivo.csv]

--split 0.7: mostra o resultado nos primeiros 70% dos dados (treino) e nos 30% finais
(fora da amostra). Escolha parametros so olhando o treino; o teste final e o que conta.
"""
import argparse

from . import backtest
from .history import fetch_history, load_csv
from .strategies import REGISTRY


def buy_and_hold(candles) -> float:
    return (candles[-1].close / candles[0].close - 1) * 100


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("symbol")
    p.add_argument("interval")
    p.add_argument("--strategy", choices=sorted(REGISTRY), default="ema_cross")
    p.add_argument("--csv")
    p.add_argument("--n", type=int, default=5000)
    p.add_argument("--capital", type=float, default=1000)
    p.add_argument("--risk", type=float, default=0.5)
    p.add_argument("--fee", type=float, default=0.1, help="taxa por lado, em %% (padrao 0.1)")
    p.add_argument("--split", type=float, default=0.0, help="fracao de treino, ex.: 0.7")
    a = p.parse_args()
    candles = load_csv(a.csv) if a.csv else fetch_history(a.symbol, a.interval, a.n)
    strat = REGISTRY[a.strategy]
    print(f"{a.strategy} | {len(candles)} candles | taxa {a.fee}%/lado")

    parts = [("total", candles)]
    if 0 < a.split < 1:
        k = int(len(candles) * a.split)
        parts = [("treino", candles[:k]), ("FORA DA AMOSTRA", candles[k:])]
    for name, chunk in parts:
        r = backtest.run(a.symbol, chunk, a.capital, a.risk, a.fee, strat)
        print(f"[{name}] {r.summary()} | buy&hold={buy_and_hold(chunk):.1f}%")


if __name__ == "__main__":
    main()
