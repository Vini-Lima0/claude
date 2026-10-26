from tradingbot.models import Candle
from tradingbot.strategy import evaluate


def candles(closes):
    return [Candle(i, c, c + 0.5, c - 0.5, c, 1) for i, c in enumerate(closes)]


def test_no_signal_when_flat():
    assert evaluate("X", candles([100] * 40)) is None


def test_buy_signal_on_upward_cross():
    closes = [100 - i * 0.3 for i in range(30)] + [91 + i * 2 for i in range(1, 12)]
    sigs = [evaluate("X", candles(closes[: n + 1])) for n in range(25, len(closes))]
    buys = [s for s in sigs if s and s.side == "BUY"]
    assert buys
    s = buys[0]
    assert s.stop < s.entry < s.target


def test_not_enough_data():
    assert evaluate("X", candles([1, 2, 3])) is None
