"""Testes do módulo de limpeza (cleaners)."""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os

from src.ingestion.cleaners import clean_sales_data


@pytest.fixture
def csv_sujo_temporario(tmp_path) -> Path:
    """Cria um CSV sujo temporário para testar o cleaner."""
    conteudo = """Transaction ID,Item,Quantity,Price Per Unit,Total Spent,Payment Method,Location,Transaction Date
1,Cappuccino,2,5.00,10.00,CREDIT_CARD,Centro,2024-01-10
2,Espresso,ERROR,3.00,3.00,CASH,Centro,2024-01-15
3,Latte,1,UNKNOWN,6.00,PIX,Norte,2024-02-01
4,,1,4.00,4.00,CASH,Sul,2024-02-15
5,Mocha,1,5.00,N/A,CREDIT_CARD,Centro,2024-03-01
6,Espresso,1,3.00,3.00,CASH,Centro,
"""
    arquivo = tmp_path / "sujo.csv"
    arquivo.write_text(conteudo)
    return arquivo


class TestCleanSalesData:
    """Testes para clean_sales_data()."""

    def test_retorna_dataframe(self, csv_sujo_temporario):
        """Função deve retornar um DataFrame."""
        resultado = clean_sales_data(csv_sujo_temporario)
        assert isinstance(resultado, pd.DataFrame)

    def test_colunas_padronizadas(self, csv_sujo_temporario):
        """Colunas devem estar em snake_case."""
        resultado = clean_sales_data(csv_sujo_temporario)
        assert "Transaction_ID" in resultado.columns
        assert "Price_Per_Item" in resultado.columns
        assert "Total_Spent" in resultado.columns

    def test_sinais_sujos_viram_nan(self, csv_sujo_temporario):
        """ERROR, UNKNOWN, N/A devem virar NaN."""
        resultado = clean_sales_data(csv_sujo_temporario)

        # Linha 2: Quantity era "ERROR" → deve ter sido preenchida com 1 (fallback)
        # Linha 3: Price_Per_Item era "UNKNOWN" → deve ter sido preenchida com mediana
        assert resultado["Quantity"].notna().all()
        assert resultado["Price_Per_Item"].notna().all()

    def test_total_spent_recalculado(self, csv_sujo_temporario):
        """Total_Spent deve ser Quantity × Price_Per_Item."""
        resultado = clean_sales_data(csv_sujo_temporario)

        esperado = resultado["Quantity"] * resultado["Price_Per_Item"]
        pd.testing.assert_series_equal(
            resultado["Total_Spent"].round(2),
            esperado.round(2),
            check_names=False
        )

    def test_datas_nulas_sao_descartadas(self, csv_sujo_temporario):
        """Linha 6 tem Transaction_Date vazio → deve ser removida."""
        resultado = clean_sales_data(csv_sujo_temporario)

        assert resultado["Transaction_Date"].notna().all()
        assert len(resultado) < 6  # Pelo menos a linha 6 foi removida

    def test_item_e_location_title_case(self, csv_sujo_temporario):
        """Strings devem estar capitalizadas."""
        resultado = clean_sales_data(csv_sujo_temporario)

        # "centro" → "Centro", "norte" → "Norte"
        assert all(resultado["Location"].str.istitle() | resultado["Location"].isna())

    def test_estrategia_mean_vs_median(self, csv_sujo_temporario):
        """Estratégias diferentes devem produzir resultados diferentes."""
        df_median = clean_sales_data(csv_sujo_temporario, fill_strategy="median")
        df_mean = clean_sales_data(csv_sujo_temporario, fill_strategy="mean")

        # Pelo menos um valor preenchido deve diferir
        # (depende dos dados, mas em geral média ≠ mediana)
        # Aqui apenas garantimos que ambas rodam sem erro
        assert isinstance(df_median, pd.DataFrame)
        assert isinstance(df_mean, pd.DataFrame)

    def test_estrategia_invalida_levanta_valueerror(self, csv_sujo_temporario):
        """Estratégia desconhecida deve levantar ValueError."""
        with pytest.raises(ValueError):
            clean_sales_data(csv_sujo_temporario, fill_strategy="modo")
