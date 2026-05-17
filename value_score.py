import yfinance as yf
import pandas as pd

acoes = [
    "PETR4.SA",
    "VALE3.SA",
    "ITUB4.SA",
    "BBAS3.SA",
    "WEGE3.SA"
]

resultado = []

for ticker in acoes:
    acao = yf.Ticker(ticker)
    info = acao.info

    pl        = info.get("trailingPE")
    pvp       = info.get("priceToBook")
    ev_ebitda = info.get("enterpriseToEbitda")
    dy        = info.get("dividendYield", 0) or 0  # sem dividendo = 0

    # Cada componente só entra no score se o valor for positivo
    componentes = []
    if pl and pl > 0:
        componentes.append(1 / pl)
    if pvp and pvp > 0:
        componentes.append(1 / pvp)
    if ev_ebitda and ev_ebitda > 0:
        componentes.append(1 / ev_ebitda)
    componentes.append(dy)  # DY entra sempre (pode ser 0)

    value_score = sum(componentes) / len(componentes)

    resultado.append({
        "Ação":       ticker,
        "P/L":        round(pl, 2)        if pl        else None,
        "P/VP":       round(pvp, 2)       if pvp       else None,
        "EV/EBITDA":  round(ev_ebitda, 2) if ev_ebitda else None,
        "DY (%)":     round(dy * 100, 2),
        "Value Score": round(value_score, 4),
    })

df = pd.DataFrame(resultado)
df = df.sort_values("Value Score", ascending=False)

print(df.to_string(index=False))
