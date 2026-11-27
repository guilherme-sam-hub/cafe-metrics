"""Testes do módulo de análise temporal."""

import pytest
import pandas as pd
from src.analytics import analise_temporal


class TestAnaliseTemporal:
    """Testes para analise_temporal()."""

    def test_retorna_dataframe_com_colunas_corretas(self, df_vendas_falso):
        """Saída deve ter exatamente as colunas esperadas."""
        resultado = analise_temporal(df_vendas_falso)

        assert isinstance(resultado, pd.DataFrame)
        assert set(resultado.columns) == {"mes", "faturamento", "variacao_pct"}

    def test_agregacao_mensal_correta(self, df_vendas_falso):
        """Faturamento mensal deve estar correto."""
        resultado = analise_temporal(df_vendas_falso)

        # Janeiro: 10 + 3 = 13
        # Fevereiro: 15 + 6 = 21
        # Março: 6 + 6 = 12
        assert resultado.loc[resultado["mes"] == "2024-01", "faturamento"].values[0] == 13.0
        assert resultado.loc[resultado["mes"] == "2024-02", "faturamento"].values[0] == 21.0
        assert resultado.loc[resultado["mes"] == "2024-03", "faturamento"].values[0] == 12.0

    def test_primeiro_mes_tem_variacao_zero(self, df_vendas_falso):
        """O primeiro mês não tem base anterior, variação deve ser 0."""
        resultado = analise_temporal(df_vendas_falso)
        assert resultado.iloc[0]["variacao_pct"] == 0.0

    def test_variacao_percentual_entre_jan_e_fev(self, df_vendas_falso):
        """(21 - 13) / 13 * 100 = 61.54%"""
        resultado = analise_temporal(df_vendas_falso)
        variacao_fev = resultado.loc[resultado["mes"] == "2024-02", "variacao_pct"].values[0]
        assert variacao_fev == pytest.approx(61.54, abs=0.01)

    def test_dataframe_vazio_retorna_schema_vazio(self, df_vendas_vazio):
        """DataFrame vazio não deve quebrar, retorna DataFrame vazio com schema."""
        resultado = analise_temporal(df_vendas_vazio)

        assert isinstance(resultado, pd.DataFrame)
        assert resultado.empty
        assert set(resultado.columns) == {"mes", "faturamento", "variacao_pct"}

    def test_coluna_faltante_levanta_keyerror(self, df_vendas_falso):
        """DataFrame sem Transaction_Date deve levantar KeyError."""
        df_sem_data = df_vendas_falso.drop(columns=["Transaction_Date"])

        with pytest.raises(KeyError):
            analise_temporal(df_sem_data)
