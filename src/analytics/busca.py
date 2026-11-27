"""
Busca de registros no dataset.
"""

from __future__ import annotations
import pandas as pd


def busca_linear(df: pd.DataFrame, chave: str, valor: any) -> pd.DataFrame:
    """
    Filtra o DataFrame retornando todas as linhas onde a coluna 'chave'
    é igual a 'valor'.

    Args:
        df: DataFrame de entrada (ex: dataset limpo).
        chave: Nome da coluna a ser buscada (ex: 'Item').
        valor: Valor a ser encontrado (ex: 'Cappuccino').

    Retorna:
        pd.DataFrame: Subconjunto de linhas que atendem ao critério.
                      Retorna vazio se nada for encontrado.

    Complexidade: O(n) — varredura vetorizada das n linhas.
    """
    # Validação rápida
    if chave not in df.columns:
        return pd.DataFrame()  # Retorna vazio se a coluna não existir

    # Filtro vetorizado do Pandas (muito mais rápido que loop for)
    # Usamos .eq() para evitar problemas com tipos mistos ou NaN
    mascara = df[chave].eq(valor)

    return df[mascara].reset_index(drop=True)
