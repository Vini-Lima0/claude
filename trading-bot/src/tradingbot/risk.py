"""Travas de risco. Ficam no codigo e valem para qualquer estrategia."""
from dataclasses import dataclass

from .models import Signal


def position_size(capital: float, risk_pct: float, entry: float, stop: float) -> float:
    """Quantidade de ativo para que, se o stop for atingido, a perda seja risk_pct do capital."""
    per_unit_risk = abs(entry - stop)
    if per_unit_risk <= 0:
        return 0.0
    return (capital * risk_pct / 100) / per_unit_risk


@dataclass
class RiskGuard:
    capital: float
    max_daily_loss_pct: float
    max_alerts_per_day: int
    daily_pnl: float = 0.0
    alerts_today: int = 0

    def allows(self, signal: Signal) -> tuple[bool, str]:
        if self.daily_pnl <= -self.capital * self.max_daily_loss_pct / 100:
            return False, "perda maxima diaria atingida"
        if self.alerts_today >= self.max_alerts_per_day:
            return False, "limite de alertas do dia atingido"
        return True, ""

    def register_alert(self) -> None:
        self.alerts_today += 1

    def reset_day(self) -> None:
        self.daily_pnl = 0.0
        self.alerts_today = 0
