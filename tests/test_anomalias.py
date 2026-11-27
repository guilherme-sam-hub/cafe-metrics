"""Testes do módulo de detecção de anomalias."""

import pytest
import pandas as pd
from src.analytics import analise_temporal, detectar_anomalias


class TestDetectarAnomalias:
    """Testes para detectar_anomalias()."""

    def test_detecta_outlier_claro(self, df_vendas_com_outlier):
        """Deve detectar julho como anomalia (faturamento ~50x maior)."""
        df_temporal = analise_temporal(df_vendas_com_outlier)
        anomalias = detectar_anomalias(df_temporal)

        assert not anomalias.empty
        assert "2024-07" in anomalias["mes"].values  # Corrigido: julho, não março


    def test_z_score_do_outlier_e_alto(self, df_vendas_com_outlier):
        """O Z-score do outlier deve ser > 2.0."""
        df_temporal = analise_temporal(df_vendas_com_outlier)
        anomalias = detectar_anomalias(df_temporal)

        z_julho = anomalias.loc[anomalias["mes"] == "2024-07", "z_score"].values[0]
        assert abs(z_julho) > 2.0

    def test_sem_anomalias_retorna_vazio(self, df_vendas_falso):
        """Dataset balanceado não deve ter anomalias com limiar padrão."""
        df_temporal = analise_temporal(df_vendas_falso)
        anomalias = detectar_anomalias(df_temporal)

        assert anomalias.empty

    def test_limiar_muito_baixo_detecta_mais(self, df_vendas_falso):
        """Com limiar 0.5, deve detectar mais anomalias."""
        df_temporal = analise_temporal(df_vendas_falso)
        anomalias = detectar_anomalias(df_temporal, limiar=0.5)

        # Com limiar baixo, pelo menos um mês deve aparecer
        assert not anomalias.empty

    def test_dataframe_vazio_retorna_vazio(self, df_vendas_vazio):
        """DataFrame vazio não deve quebrar."""
        anomalias = detectar_anomalias(df_vendas_vazio)
        assert anomalias.empty

    def test_coluna_z_score_presente(self, df_vendas_com_outlier):
        """Saída deve incluir a coluna z_score."""
        df_temporal = analise_temporal(df_vendas_com_outlier)
        anomalias = detectar_anomalias(df_temporal)

        assert "z_score" in anomalias.columns
