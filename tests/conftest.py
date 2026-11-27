"""
Fixtures compartilhadas para todos os testes.
O pytest injeta automaticamente estas fixtures nos testes que as solicitarem.
"""

import pandas as pd
import pytest


@pytest.fixture
def df_vendas_falso() -> pd.DataFrame:
    """
    DataFrame sintético com 6 vendas distribuídas em 3 meses.
    Permite testar agregações, filtros e cálculos de forma determinística.
    """
    return pd.DataFrame({
        "Transaction_ID": [1, 2, 3, 4, 5, 6],
        "Item": ["Cappuccino", "Espresso", "Cappuccino", "Latte", "Espresso", "Latte"],
        "Quantity": [2, 1, 3, 1, 2, 1],
        "Price_Per_Item": [5.0, 3.0, 5.0, 6.0, 3.0, 6.0],
        "Total_Spent": [10.0, 3.0, 15.0, 6.0, 6.0, 6.0],
        "Payment_Method": ["CREDIT_CARD", "CASH", "CREDIT_CARD", "PIX", "CASH", "PIX"],
        "Location": ["Centro", "Centro", "Norte", "Norte", "Centro", "Sul"],
        "Transaction_Date": pd.to_datetime([
            "2024-01-10", "2024-01-15",
            "2024-02-05", "2024-02-20",
            "2024-03-01", "2024-03-15",
        ]),
    })


@pytest.fixture
def df_vendas_vazio() -> pd.DataFrame:
    """DataFrame vazio com schema correto (para testar edge cases)."""
    return pd.DataFrame({
        "Transaction_ID": pd.Series(dtype=int),
        "Item": pd.Series(dtype=str),
        "Quantity": pd.Series(dtype=int),
        "Price_Per_Item": pd.Series(dtype=float),
        "Total_Spent": pd.Series(dtype=float),
        "Payment_Method": pd.Series(dtype=str),
        "Location": pd.Series(dtype=str),
        "Transaction_Date": pd.Series(dtype="datetime64[ns]"),
    })


@pytest.fixture
def df_vendas_com_outlier() -> pd.DataFrame:
    """
    DataFrame com outlier claro em julho (faturamento ~50x maior).
    Série longa (12 meses, 29 vendas) para que o outlier não infle o desvio padrão.
    """
    # 12 meses de dados
    meses = [
        "2024-01-05", "2024-01-20",       # Jan: 2 vendas
        "2024-02-10", "2024-02-25",       # Fev: 2 vendas
        "2024-03-05", "2024-03-15",       # Mar: 2 vendas
        "2024-04-01", "2024-04-20",       # Abr: 2 vendas
        "2024-05-10", "2024-05-25",       # Mai: 2 vendas
        "2024-06-05", "2024-06-20",       # Jun: 2 vendas
        # Julho: 7 vendas (uma delas é o outlier)
        "2024-07-01", "2024-07-10", "2024-07-15", "2024-07-20",
        "2024-07-25", "2024-07-28", "2024-07-30",
        # Volta ao normal
        "2024-08-05", "2024-08-20",       # Ago: 2 vendas
        "2024-09-10", "2024-09-25",       # Set: 2 vendas
        "2024-10-05", "2024-10-20",       # Out: 2 vendas
        "2024-11-10", "2024-11-25",       # Nov: 2 vendas
        "2024-12-05", "2024-12-20",       # Dez: 2 vendas
    ]

    # 29 vendas no total. Outlier na posição 15 (quarta venda de julho)
    # Índices 0-14: $5 (15 vendas normais)
    # Índice 15: $500 (outlier em julho)
    # Índices 16-28: $5 (13 vendas normais)
    precos = [5.0] * 15 + [500.0] + [5.0] * 13
    quantities = [1] * 29

    return pd.DataFrame({
        "Transaction_ID": range(1, 30),
        "Item": ["Cappuccino"] * 29,
        "Quantity": quantities,
        "Price_Per_Item": precos,
        "Total_Spent": precos,  # Como Qtd=1, Total = Price
        "Payment_Method": ["CASH"] * 29,
        "Location": ["Centro"] * 29,
        "Transaction_Date": pd.to_datetime(meses),
    })

    # 28 vendas normais de $5 + 1 venda outlier de $500 = 29 vendas no total
    precos = [5.0] * 28 + [500.0]
    quantities = [1] * 29

    return pd.DataFrame({
        "Transaction_ID": range(1, 30),
        "Item": ["Cappuccino"] * 29,
        "Quantity": quantities,
        "Price_Per_Item": precos,
        "Total_Spent": precos,  # Como Qtd=1, Total = Price
        "Payment_Method": ["CASH"] * 29,
        "Location": ["Centro"] * 29,
        "Transaction_Date": pd.to_datetime(meses),
    })
