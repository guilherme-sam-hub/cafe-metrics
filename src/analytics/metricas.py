"""
Cálculos estatísticos puros de KPIs — sem I/O, sem prints.
"""

from __future__ import annotations
import pandas as pd


def calcular_kpis(df: pd.DataFrame, filtros: dict | None = None) -> dict:
    """
    Calcula os KPIs principais do dashboard.

    Retorna um dict com ``faturamento_total``, ``ticket_medio`` e
    ``total_itens_vendidos``. Se o filtro não casar nenhuma linha,
    retorna ``{"erro": "..."}`` para que a camada de apresentação trate.
    """
    df_trabalho = df.copy()

    if filtros:
        for col, val in filtros.items():
            # .isin() ou == dependendo se o filtro for lista ou escalar,

            df_trabalho = df_trabalho[df_trabalho[col] == val]

    if df_trabalho.empty:
        return {"erro": "Nenhum registro corresponde aos filtros aplicados."}

    return {
        "faturamento_total": float(df_trabalho["Total_Spent"].sum()),
        "ticket_medio": float(df_trabalho["Total_Spent"].mean()),
        "total_itens_vendidos": int(df_trabalho["Quantity"].sum()),
    }
