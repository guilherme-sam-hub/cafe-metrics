"""Testes do módulo de ordenação/ranking."""

import pytest
import pandas as pd
from src.analytics import ordenar_por_vendas


class TestOrdenarPorVendas:
    """Testes para ordenar_por_vendas()."""

    def test_retorna_dataframe_com_colunas_corretas(self, df_vendas_falso):
        """Saída deve ter Item e Total_Vendido."""
        resultado = ordenar_por_vendas(df_vendas_falso)

        assert isinstance(resultado, pd.DataFrame)
        assert set(resultado.columns) == {"Item", "Total_Vendido"}

    def test_ordenacao_decrescente(self, df_vendas_falso):
        """Produtos devem vir do mais vendido para o menos vendido."""
        resultado = ordenar_por_vendas(df_vendas_falso)

        # Cappuccino: 2+3 = 5
        # Espresso: 1+2 = 3
        # Latte: 1+1 = 2
        assert resultado.iloc[0]["Item"] == "Cappuccino"
        assert resultado.iloc[0]["Total_Vendido"] == 5
        assert resultado.iloc[1]["Item"] == "Espresso"
        assert resultado.iloc[2]["Item"] == "Latte"

    def test_dataframe_vazio_retorna_schema_vazio(self, df_vendas_vazio):
        """DataFrame vazio retorna DataFrame vazio com schema correto."""
        resultado = ordenar_por_vendas(df_vendas_vazio)

        assert resultado.empty
        assert set(resultado.columns) == {"Item", "Total_Vendido"}
