# trading-bot

Monitor de day trade que gera **alertas** (entrada, stop, alvo e tamanho de posicao) para cripto e, depois, B3.
Nesta fase **nao envia ordens**: voce executa manualmente na corretora.

## Rodar

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencha o Telegram se quiser alertas no celular
PYTHONPATH=src python -m tradingbot.main
pytest
```

Sem Telegram configurado, os alertas aparecem no terminal.

## Estrutura

- `strategy.py`: regra de sinal (exemplo: cruzamento EMA9/EMA21 + stop por ATR). Troque pela sua.
- `risk.py`: tamanho de posicao, perda maxima diaria e limite de alertas.
- `sources/binance.py`: candles publicos da Binance (sem chave).
- `notifier.py`: Telegram ou terminal.

## Proximas etapas

1. Backtest da estrategia com historico.
2. Fonte de dados da B3 via MetaTrader 5 (pacote `MetaTrader5` e **somente Windows**) na conta demo da Clear.
3. Execucao com confirmacao na Binance Testnet / MT5 demo.
4. Automatico em conta real so apos validacao longa e com valores pequenos.

A estrategia de exemplo nao tem lucratividade comprovada. Day trade envolve risco real de perda.

## Backtest

```bash
PYTHONPATH=src python -m tradingbot.backtest_cli BTCUSDT 5m --n 5000
PYTHONPATH=src python -m tradingbot.backtest_cli WINZ25 5m --csv historico.csv   # CSV: open_time,open,high,low,close,volume
```

Entra na abertura do candle seguinte ao sinal, desconta taxa de 0,1% por lado e, se stop e alvo
forem tocados no mesmo candle, assume o stop.
