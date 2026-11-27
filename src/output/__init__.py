"""
Camada de Output (Adapters): renderização dos dados do Core Analytics.

Responsável por traduzir DataFrames e dicts em interfaces visuais:
  - Terminal (CLI) via Rich
  - Arquivos PNG estáticos via Matplotlib
  - Dashboard web interativo via Streamlit + Plotly

Este módulo re-exporta as funções públicas dos adapters para permitir
imports limpos nos entry points (main.py e app_web.py).
"""

from __future__ import annotations


# CLI Adapter (Terminal com Rich)
from .cli_adapter import (
    exibir_kpis_terminal,
    exibir_analise_temporal_terminal,
    exibir_anomalias_terminal,
    exibir_busca_terminal,
    exibir_ranking_terminal,
    exibir_sucesso_salvamento,
)


# Matplotlib Adapter (PNGs estáticos)
from .matplotlib_adapter import gerar_e_salvar_graficos


# Streamlit Adapter (Dashboard web interativo)
from .streamlit_adapter import (
    renderizar_dashboard_web,
    renderizar_kpis,
    renderizar_grafico_temporal,
    renderizar_grafico_barras,
    renderizar_grafico_pagamentos,
)


# API Pública

__all__ = [
    # CLI Adapter
    "exibir_kpis_terminal",
    "exibir_analise_temporal_terminal",
    "exibir_anomalias_terminal",
    "exibir_busca_terminal",
    "exibir_ranking_terminal",
    "exibir_sucesso_salvamento",

    # Matplotlib Adapter
    "gerar_e_salvar_graficos",

    # Streamlit Adapter
    "renderizar_dashboard_web",
    "renderizar_kpis",
    "renderizar_grafico_temporal",
    "renderizar_grafico_barras",
    "renderizar_grafico_pagamentos",
]
