from tradingbot import backtest
from tradingbot.models import Candle


def mk(closes):
    return [Candle(i, c, c + 0.5, c - 0.5, c, 1) for i, c in enumerate(closes)]


def test_flat_market_has_no_trades():
    r = backtest.run("X", mk([100] * 80))
    assert r.trades == [] and r.end_capital == r.start_capital


def test_trend_produces_trades_and_consistent_equity():
    closes = [100 - i * 0.3 for i in range(40)] + [88 + i * 1.5 for i in range(60)] + \
             [178 - i * 1.5 for i in range(60)]
    r = backtest.run("X", mk(closes))
    assert r.trades
    assert abs(r.end_capital - (r.start_capital + sum(t.pnl for t in r.trades))) < 1e-6
    assert 0 <= r.win_rate <= 1 and r.max_drawdown_pct >= 0


def test_stop_wins_when_both_hit_same_candle():
    c = Candle(0, 100, 110, 90, 100, 1)
    assert backtest._exit_price("BUY", stop=95, target=105, c=c) == 95
