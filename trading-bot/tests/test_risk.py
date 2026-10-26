from tradingbot.models import Signal
from tradingbot.risk import RiskGuard, position_size

SIG = Signal("BTCUSDT", "BUY", 100, 99, 102, "teste")


def test_position_size_risks_expected_amount():
    qty = position_size(1000, 0.5, entry=100, stop=98)
    assert qty == 2.5  # risco de 5 / 2 por unidade
    assert qty * 2 == 1000 * 0.5 / 100


def test_position_size_zero_distance():
    assert position_size(1000, 1, 100, 100) == 0.0


def test_daily_loss_blocks():
    g = RiskGuard(1000, 2, 10, daily_pnl=-20)
    ok, _ = g.allows(SIG)
    assert not ok


def test_alert_limit_blocks_and_reset():
    g = RiskGuard(1000, 2, 1)
    assert g.allows(SIG)[0]
    g.register_alert()
    assert not g.allows(SIG)[0]
    g.reset_day()
    assert g.allows(SIG)[0]
