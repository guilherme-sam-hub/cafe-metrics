"""
Detecção de anomalias em séries temporais usando Z-Score.
"""

from __future__ import annotations
import pandas as pd


def detectar_anomalias(
    df_temporal: pd.DataFrame,
    limiar: float = 2.0
) -> pd.DataFrame:
    """
    Sinaliza meses cujo faturamento está a mais de ``limiar`` desvios padrão
    da média.

    Args:
        df_temporal: DataFrame de saída da função ``analise_temporal``.
                     Deve conter a coluna ``faturamento``.
        limiar: Valor de corte para o Z-Score (padrão 2.0).

    Retorna:
        pd.DataFrame: Contendo apenas as anomalias, com a coluna ``z_score``
                      adicionada. Retorna vazio se não houver anomalias.

    Observações:
      - Usa desvio padrão POPULACIONAL (ddof=0), tratando a série como
        o universo completo.
      - Séries curtas (< 2 meses) ou com desvio zero retornam vazio.
    """
    # 1. Validação e Edge Cases
    if df_temporal.empty or len(df_temporal) < 2:
        return pd.DataFrame(columns=[*df_temporal.columns, "z_score"])

    # 2. Cálculo dos parâmetros estatísticos
    # ddof=0 garante o desvio padrão POPULACIONAL (equivalente a statistics.pstdev)
    media = df_temporal["faturamento"].mean()
    desvio = df_temporal["faturamento"].std(ddof=0)

    # Se o desvio for 0, todos os valores são iguais -> não há anomalias
    if desvio == 0 or pd.isna(desvio):
        return pd.DataFrame(columns=[*df_temporal.columns, "z_score"])

    # 3. Cálculo vetorizado do Z-Score
    df_anomalias = df_temporal.copy()
    df_anomalias["z_score"] = (
        (df_anomalias["faturamento"] - media) / desvio
    ).round(2)

    # 4. Filtragem
    anomalias_filtradas = df_anomalias[df_anomalias["z_score"].abs() > limiar]

    return anomalias_filtradas.reset_index(drop=True)
