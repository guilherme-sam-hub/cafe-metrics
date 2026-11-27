"""
Adapter de Streamlit: renderiza dashboard web interativo com Plotly.
Responsável por formatar e exibir os dados do Core Analytics via Streamlit.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from ..analytics import analise_temporal, calcular_kpis


# HELPERS DE FORMATAÇÃO

def _formatar_moeda(valor: float) -> str:
    """Formata float para moeda BRL (ex: R$ 1.234,56)."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# COMPONENTES DE RENDERIZAÇÃO

def renderizar_kpis(kpis: dict, filtros: dict | None = None) -> None:
    """
    Renderiza cards de KPI no Streamlit.
    Trata o caso de erro retornado pelo Core.
    """
    if filtros:
        st.sidebar.markdown(f"**🔍 Filtros ativos:** {filtros}")

    # Tratamento do caso de erro
    if "erro" in kpis:
        st.error(f"⚠️ {kpis['erro']}")
        return

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="💰 Faturamento Total",
            value=_formatar_moeda(kpis['faturamento_total'])
        )

    with col2:
        st.metric(
            label="🎫 Ticket Médio",
            value=_formatar_moeda(kpis['ticket_medio'])
        )

    with col3:
        st.metric(
            label="📦 Itens Vendidos",
            value=f"{kpis['total_itens_vendidos']:,} un"
        )


def renderizar_grafico_temporal(df_temp: pd.DataFrame) -> None:
    """
    Renderiza gráfico de linha temporal.
    Colunas esperadas: 'mes' e 'faturamento'.
    """
    if df_temp.empty:
        st.info("📊 Nenhum dado temporal disponível para os filtros selecionados.")
        return

    fig = px.line(
        df_temp,
        x="mes",
        y="faturamento",
        markers=True,
        template="plotly_white",
        title="Tendência Temporal do Faturamento Mensal"
    )
    fig.update_traces(line_color="#529286", marker_size=8)
    st.plotly_chart(fig, use_container_width=True)


def renderizar_grafico_barras(df: pd.DataFrame) -> None:
    """
    Renderiza gráfico de barras de faturamento por categoria.
    """
    if df.empty:
        st.info("📊 Nenhum dado para exibir.")
        return

    # Agregação (trivial, aceitável no adapter)
    df_agrupado = (
        df.groupby("Item")["Total_Spent"]
        .sum()
        .reset_index()
        .sort_values("Total_Spent", ascending=False)
    )

    fig = px.bar(
        df_agrupado,
        x="Item",
        y="Total_Spent",
        template="plotly_white",
        title="Faturamento por Categoria de Item",
        color_discrete_sequence=["#529286"]
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)


def renderizar_grafico_pagamentos(df: pd.DataFrame) -> None:
    """
    Renderiza gráfico de rosca (donut) de métodos de pagamento.
    """
    if df.empty or "Payment_Method" not in df.columns:
        st.info("📊 Nenhum dado de pagamento disponível.")
        return

    df_pagamentos = (
        df.groupby("Payment_Method")["Transaction_ID"]
        .count()
        .reset_index()
    )

    fig = px.pie(
        df_pagamentos,
        names="Payment_Method",
        values="Transaction_ID",
        hole=0.4,
        template="plotly_white",
        title="Preferência de Métodos de Pagamento",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)

# FILTROS (SIDEBAR)

def _montar_filtros(df: pd.DataFrame) -> dict:
    """
    Renderiza seletores na sidebar e retorna dict de filtros ativos.
    """
    st.sidebar.header("🔍 Filtros de Negócio")

    filtros = {}

    # Filtro de Filial
    locais = ["Todos"] + sorted(df["Location"].dropna().unique().tolist())
    local = st.sidebar.selectbox("Filial:", locais)
    if local != "Todos":
        filtros["Location"] = local

    # Filtro de Produto
    itens = ["Todos"] + sorted(df["Item"].dropna().unique().tolist())
    item = st.sidebar.selectbox("Produto:", itens)
    if item != "Todos":
        filtros["Item"] = item

    return filtros

# ORQUESTRADOR PRINCIPAL

def renderizar_dashboard_web(df_limpo: pd.DataFrame) -> None:
    """
    Função principal que orquestra todo o dashboard.

    Pré-requisitos:
      - Deve ser chamada APÓS st.set_page_config() no app_web.py.
      - df_limpo deve conter as colunas: Item, Location, Total_Spent,
        Payment_Method, Transaction_ID, Transaction_Date.
    """
    st.title("☕ Cafe Sales - Dashboard de Métricas")
    st.markdown("---")

    # 1. Monta filtros na sidebar
    filtros = _montar_filtros(df_limpo)

    # 2. Aplica filtros nos dados
    df_filtrado = df_limpo.copy()
    for col, val in filtros.items():
        df_filtrado = df_filtrado[df_filtrado[col] == val]

    # 3. Renderiza KPIs
    kpis = calcular_kpis(df_filtrado)
    renderizar_kpis(kpis, filtros if filtros else None)

    st.markdown("---")

    # 4. Renderiza gráficos em colunas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🛍️ Faturamento por Categoria")
        renderizar_grafico_barras(df_filtrado)

    with col2:
        st.subheader("💳 Métodos de Pagamento")
        renderizar_grafico_pagamentos(df_filtrado)

    st.markdown("---")

    # 5. Renderiza gráfico temporal (linha completa)
    st.subheader("📈 Evolução Temporal")
    df_temporal = analise_temporal(df_filtrado)
    renderizar_grafico_temporal(df_temporal)
