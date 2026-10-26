"""Backtest simples: entra na abertura do candle seguinte ao sinal (sem look-ahead).

Se stop e alvo forem tocados no mesmo candle, assume o stop (hipotese conservadora).
"""
from dataclasses import dataclass

from .models import Candle
from .risk import position_size
from .strategy import evaluate

WARMUP = 30


@dataclass
class Trade:
    side: str
    entry: float
    exit: float
    qty: float
    pnl: float
    r_multiple: float


@dataclass
class Result:
    trades: list[Trade]
    start_capital: float
    end_capital: float
    max_drawdown_pct: float

    @property
    def win_rate(self) -> float:
        return sum(t.pnl > 0 for t in self.trades) / len(self.trades) if self.trades else 0.0

    def summary(self) -> str:
        ret = (self.end_capital / self.start_capital - 1) * 100
        avg_r = sum(t.r_multiple for t in self.trades) / len(self.trades) if self.trades else 0.0
        return (
            f"trades={len(self.trades)} win_rate={self.win_rate:.1%} avg_R={avg_r:.2f} "
            f"retorno={ret:.2f}% max_drawdown={self.max_drawdown_pct:.2f}%"
        )


def _exit_price(side: str, stop: float, target: float, c: Candle) -> float | None:
    if side == "BUY":
        if c.low <= stop:
            return stop
        if c.high >= target:
            return target
    else:
        if c.high >= stop:
            return stop
        if c.low <= target:
            return target
    return None


def run(symbol: str, candles: list[Candle], capital: float = 1000.0,
        risk_pct: float = 0.5, fee_pct: float = 0.1) -> Result:
    equity = start = capital
    peak, max_dd = equity, 0.0
    trades: list[Trade] = []
    i = WARMUP
    while i < len(candles) - 1:
        sig = evaluate(symbol, candles[: i + 1])
        if not sig:
            i += 1
            continue
        entry = candles[i + 1].open
        shift = entry - sig.entry  # reaplica a distancia de stop/alvo ao preco real de entrada
        stop, target = sig.stop + shift, sig.target + shift
        qty = position_size(equity, risk_pct, entry, stop)
        j, exit_px = i + 1, None
        while j < len(candles):
            exit_px = _exit_price(sig.side, stop, target, candles[j])
            if exit_px is not None:
                break
            j += 1
        if exit_px is None:
            break  # posicao ainda aberta no fim dos dados: ignora
        direction = 1 if sig.side == "BUY" else -1
        fees = (entry + exit_px) * qty * fee_pct / 100
        pnl = (exit_px - entry) * direction * qty - fees
        risk_amt = abs(entry - stop) * qty
        equity += pnl
        trades.append(Trade(sig.side, entry, exit_px, qty, pnl, pnl / risk_amt if risk_amt else 0.0))
        peak = max(peak, equity)
        max_dd = max(max_dd, (peak - equity) / peak * 100)
        i = j + 1
    return Result(trades, start, equity, max_dd)
