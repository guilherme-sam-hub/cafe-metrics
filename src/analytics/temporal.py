"""
Análise de série temporal e variações percentuais.

Regra de negócio: vendas sem data são descartadas (inúteis para série temporal).
"""

from __future__ import annotations
import pandas as pd


def analise_temporal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna DataFrame mensal com faturamento e variação percentual.

    Colunas de saída: ``mes``, ``faturamento``, ``variacao_pct``.

    Contratos:
      - O primeiro mês tem ``variacao_pct = 0.0`` (não há base anterior).
      - Linhas com ``Transaction_Date`` nulo são descartadas.
      - DataFrame vazio na entrada retorna DataFrame vazio na saída (não quebra).

    Pré-requisitos: colunas ``Transaction_Date`` (datetime64) e ``Total_Spent`` (float).

    Complexidade: O(n) no groupby + O(m) na variação (m = nº de meses).
    """
    # Fail fast: valida colunas obrigatórias
    colunas_obrigatorias = {"Transaction_Date", "Total_Spent"}
    faltantes = colunas_obrigatorias - set(df.columns)
    if faltantes:
        raise KeyError(
            f"analise_temporal: colunas faltantes {faltantes}. "
            f"Disponíveis: {list(df.columns)}"
        )

    # Filtra datas nulas e cria a coluna de período (YYYY-MM)
    df_temp = df.dropna(subset=["Transaction_Date"]).assign(
        mes=df["Transaction_Date"].dt.to_period("M").astype(str)
    )

    # Se não sobrou nada após o dropna, retorna vazio com schema correto
    if df_temp.empty:
        return pd.DataFrame(columns=["mes", "faturamento", "variacao_pct"])

    # Agrega faturamento por mês
    serie = (
        df_temp.groupby("mes")["Total_Spent"]
        .sum()
        .reset_index(name="faturamento")
        .sort_values("mes")
        .reset_index(drop=True)
    )

    # Variação percentual mês a mês
    # fill_method=None evita deprecation warning no Pandas 2.2+
    serie["variacao_pct"] = (
        serie["faturamento"]
        .pct_change(fill_method=None)
        .mul(100)
        .round(2)
        .fillna(0.0)  # Primeiro mês não tem base anterior
    )

    return serie
