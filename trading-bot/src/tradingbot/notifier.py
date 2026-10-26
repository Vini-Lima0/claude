import requests

from .models import Signal


def format_signal(signal: Signal, qty: float) -> str:
    return (
        f"{signal.side} {signal.symbol}\n"
        f"Motivo: {signal.reason}\n"
        f"Entrada: {signal.entry:.2f}\n"
        f"Stop: {signal.stop:.2f}\n"
        f"Alvo: {signal.target:.2f}\n"
        f"Quantidade sugerida: {qty:.6f}"
    )


class Notifier:
    def __init__(self, token: str, chat_id: str):
        self.token, self.chat_id = token, chat_id

    def send(self, text: str) -> None:
        if not (self.token and self.chat_id):
            print(text)  # sem Telegram configurado: imprime no terminal
            return
        requests.post(
            f"https://api.telegram.org/bot{self.token}/sendMessage",
            json={"chat_id": self.chat_id, "text": text},
            timeout=10,
        ).raise_for_status()
