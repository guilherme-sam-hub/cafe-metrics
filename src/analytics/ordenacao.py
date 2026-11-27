"""
Ranking e ordenação de produtos por volume de vendas.
"""

from __future__ import annotations
import pandas as pd


def ordenar_por_vendas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega a quantidade vendida por produto e ordena do MAIS para o MENOS vendido.

    Args:
        df: DataFrame de entrada contendo as colunas 'Item' e 'Quantity'.

    Retorna:
        pd.DataFrame: Duas colunas ['Item', 'Total_Vendido'], ordenado decrescente.

    Complexidade: O(n) para agregação + O(p log p) para ordenação (Timsort).
    """
    # Validação de colunas
    if "Item" not in df.columns or "Quantity" not in df.columns:
        return pd.DataFrame(columns=["Item", "Total_Vendido"])

    # 1. Agregação (groupby) + Ordenação (sort_values)
    ranking = (
        df.groupby("Item")["Quantity"]
        .sum()
        .reset_index()
        .rename(columns={"Quantity": "Total_Vendido"})
        .sort_values(by="Total_Vendido", ascending=False)
        .reset_index(drop=True)
    )

    return ranking
