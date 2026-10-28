import streamlit as st
import plotly.express as px
import pandas as pd
from ..analytics.statistics import calcular_metricas_vendas


def renderizar_dashboard_web(df_limpo: pd.DataFrame) -> None:
    """
    Renderiza um painel rico e interativo no navegador web utilizando Streamlit e Plotly.
    """
    # 1. Configurações da Página Web
    st.set_page_config(page_title="Cafe Sales Analytics", page_icon="☕", layout="wide")

    st.title("☕ Cafe Sales - Dashboard de Métricas")
    st.markdown("---")

    # 2. Barra Lateral de Filtros Dinâmicos (Sincronizados com o nosso **kwargs do Analytics)
    st.sidebar.header("🔍 Filtros de Negócio")

    # Criamos os seletores web alimentados com os dados reais do dataset
    locais_disponiveis = ["Todos"] + list(df_limpo["Location"].unique())
    local_selecionado = st.sidebar.selectbox("Selecione a Filial:", locais_disponiveis)

    itens_disponiveis = ["Todos"] + list(df_limpo["Item"].unique())
    item_selecionado = st.sidebar.selectbox("Selecione o Produto:", itens_disponiveis)

    # Montamos o dicionário de filtros dinâmicos de forma opcional
    filtros = {}
    if local_selecionado != "Todos":
        filtros["Location"] = local_selecionado
    if item_selecionado != "Todos":
        filtros["Item"] = item_selecionado

    # 3. Consumindo o Motor Estatístico Existente do Monolito
    # Passamos os filtros desempacotados em formato **kwargs exatamente como no terminal
    metricas = calcular_metricas_vendas(df_limpo, **filtros)

    # Se o filtro não retornar dados, o Streamlit avisa amigavelmente
    if "erro" in metricas:
        st.error(f"⚠️ {metricas['erro']}")
        return

    # 4. Renderizando os Cartões de KPIs (Indicadores Principais)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="💰 Faturamento Total", value=f"$ {metricas.get('faturamento_total', 0):,.2f}")
    with col2:
        st.metric(label="🎫 Ticket Médio por Venda", value=f"$ {metricas.get('ticket_medio', 0):,.2f}")
    with col3:
        st.metric(label="📦 Volume de Itens Vendidos", value=f"{metricas.get('total_itens_vendidos', 0):,} un")

    st.markdown("---")

    # 5. Adicionando Gráficos Interativos (Plotly)
    # Filtramos o DataFrame base de forma visual para desenhar os gráficos na tela
    df_grafico = df_limpo.copy()
    for col, val in filtros.items():
        df_grafico = df_grafico[df_grafico[col] == val]

    graf_col1, graf_col2 = st.columns(2)

    with graf_col1:
        st.subheader("🛍️ Faturamento por Categoria de Item")
        # Agrupa os dados e gera um gráfico de barras verticais elegante
        faturamento_por_item = df_grafico.groupby("Item")["Total_Spent"].sum().reset_index()
        fig_barras = px.bar(faturamento_por_item, x="Item", y="Total_Spent",
                            labels={"Total_Spent": "Faturamento ($)"}, template="plotly_white", color="Item")
        st.plotly_chart(fig_barras, use_container_width=True)

    with graf_col2:
        st.subheader("💳 Preferência de Métodos de Pagamento")
        # Gera um gráfico de rosca (pizza vazada) dinâmico
        pagamentos = df_grafico.groupby("Payment_Method")["Transaction_ID"].count().reset_index()
        fig_rosca = px.pie(pagamentos, values="Transaction_ID", names="Payment_Method",
                           hole=0.4, template="plotly_white", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_rosca, use_container_width=True)
