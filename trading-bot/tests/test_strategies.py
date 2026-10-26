from tradingbot.models import Candle
from tradingbot.strategies import REGISTRY, donchian_breakout, rsi, trend_pullback


def mk(closes):
    return [Candle(i, c, c + 0.5, c - 0.5, c, 1) for i, c in enumerate(closes)]


def test_rsi_bounds():
    assert rsi([1.0 * i for i in range(1, 40)]) == 100.0
    assert rsi([100 - i for i in range(40)]) < 5


def test_donchian_fires_on_breakout_in_uptrend():
    closes = [100 + i * 0.1 for i in range(150)] + [110, 110, 110, 110, 125]
    s = donchian_breakout("X", mk(closes))
    assert s and s.side == "BUY" and s.stop < s.entry < s.target


def test_donchian_ignores_downtrend():
    closes = [200 - i * 0.5 for i in range(150)] + [126, 126, 126, 126, 140]
    assert donchian_breakout("X", mk(closes)) is None


def test_pullback_needs_uptrend():
    down = [200 - i for i in range(150)]
    assert trend_pullback("X", mk(down)) is None


def test_registry_strategies_handle_short_history():
    for f in REGISTRY.values():
        assert f("X", mk([1, 2, 3])) is None
