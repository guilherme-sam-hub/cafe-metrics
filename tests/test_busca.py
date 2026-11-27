"""Testes do módulo de busca."""

import pytest
import pandas as pd
from src.analytics import busca_linear


class TestBuscaLinear:
    """Testes para busca_linear()."""

    def test_busca_por_item_existente(self, df_vendas_falso):
        """Buscar 'Cappuccino' deve retornar 2 vendas."""
        resultado = busca_linear(df_vendas_falso, chave="Item", valor="Cappuccino")

        assert isinstance(resultado, pd.DataFrame)
        assert len(resultado) == 2
        assert all(resultado["Item"] == "Cappuccino")

    def test_busca_por_item_inexistente_retorna_vazio(self, df_vendas_falso):
        """Buscar item inexistente retorna DataFrame vazio."""
        resultado = busca_linear(df_vendas_falso, chave="Item", valor="Chá")

        assert isinstance(resultado, pd.DataFrame)
        assert resultado.empty

    def test_busca_por_local(self, df_vendas_falso):
        """Buscar por Location deve funcionar."""
        resultado = busca_linear(df_vendas_falso, chave="Location", valor="Centro")

        assert len(resultado) == 3  # IDs 1, 2, 5

    def test_coluna_inexistente_retorna_vazio(self, df_vendas_falso):
        """Chave que não existe no DataFrame retorna vazio (fail-safe)."""
        resultado = busca_linear(df_vendas_falso, chave="ColunaFantasma", valor="x")

        assert resultado.empty
