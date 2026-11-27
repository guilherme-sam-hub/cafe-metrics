"""
Adapter de Matplotlib: converte DataFrames em gráficos PNG estáticos.
Responsável apenas pela renderização visual, delegando cálculos ao Core.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Backend headless — DEVE vir antes de pyplot
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter  # Para formatar eixos

from ..analytics import analise_temporal  # Corrigido: nome da função no temporal.py
from ..core import config


def _formatar_eixo_y(valor, pos):
    """Helper para formatar ticks do eixo Y com separadores de milhar."""
    return f"${valor:,.0f}"


def gerar_e_salvar_graficos(df: pd.DataFrame) -> list[str]:
    """
    Gera dois gráficos PNG a partir do DataFrame limpo de vendas.

    1. Linha: Faturamento mensal (usa ``analise_temporal`` do Core).
    2. Barras: Faturamento total por categoria de item.

    Retorna lista com os caminhos absolutos dos arquivos gerados.
    Levanta ``ValueError`` se o DataFrame estiver vazio.
    """
    if df.empty:
        raise ValueError("DataFrame vazio — não há dados para gerar gráficos.")

    config.EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    destino: Path = config.EXPORTS_DIR
    caminhos: list[str] = []

    # --- 1. Linha: tendência temporal ------------------------------------
    # Delega o cálculo pesado para o Core
    serie_temporal = analise_temporal(df)

    if not serie_temporal.empty:
        fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)

        ax.plot(
            serie_temporal["mes"],
            serie_temporal["faturamento"],
            marker="o",
            linewidth=2,
            color="#529286"  # Mantendo a identidade visual do projeto
        )

        ax.set_title("Tendência Temporal do Faturamento Mensal", fontsize=14, fontweight="bold")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Faturamento ($)")

        # Formatação profissional do eixo Y
        ax.yaxis.set_major_formatter(FuncFormatter(_formatar_eixo_y))
        ax.tick_params(axis="x", rotation=45)

        caminho_linha = destino / "faturamento_linha.png"
        fig.savefig(caminho_linha, dpi=120)
        plt.close(fig)  # Libera memória
        caminhos.append(str(caminho_linha))

    # --- 2. Barras: faturamento por categoria ----------------------------
    # Agregação simples (aceitável no adapter por ser trivial)
    por_item = (
        df.groupby("Item")["Total_Spent"]
        .sum()
        .sort_values(ascending=False)
    )

    if not por_item.empty:
        fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)

        ax.bar(por_item.index, por_item.values, color="#529286")

        ax.set_title("Faturamento por Categoria de Item", fontsize=14, fontweight="bold")
        ax.set_xlabel("Item")
        ax.set_ylabel("Faturamento ($)")

        # Formatação profissional do eixo Y
        ax.yaxis.set_major_formatter(FuncFormatter(_formatar_eixo_y))
        ax.tick_params(axis="x", rotation=45)

        caminho_barras = destino / "faturamento_barras.png"
        fig.savefig(caminho_barras, dpi=120)
        plt.close(fig)  # Libera memória
        caminhos.append(str(caminho_barras))

    return caminhos
