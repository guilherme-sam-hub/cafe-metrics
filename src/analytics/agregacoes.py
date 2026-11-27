# src/analytics/agregacoes.py
import pandas as pd

def calcular_tendencia_mensal(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna um DF com [Mes, Faturamento]. Agnóstico a gráficos."""
    df_temp = df.copy()
    df_temp["Ano_Mes"] = df_temp["Transaction_Date"].dt.to_period("M").astype(str)
    return (
        df_temp.groupby("Ano_Mes")["Total_Spent"]
        .sum()
        .reset_index()
        .sort_values("Ano_Mes")
    )

def calcular_faturamento_por_item(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna um DF com [Item, Faturamento]. Agnóstico a gráficos."""
    return (
        df.groupby("Item")["Total_Spent"]
        .sum()
        .reset_index()
        .sort_values("Total_Spent", ascending=False)
    )
