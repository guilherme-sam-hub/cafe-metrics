"""
Entry point do dashboard web do Cafe Sales.

Execute com:
    streamlit run app_web.py

Não use `python app_web.py` — Streamlit exige o comando `streamlit run`.
"""

from __future__ import annotations

import streamlit as st

from src.ingestion import garantir_dataset_local, clean_sales_data
from src.output import renderizar_dashboard_web


@st.cache_data(show_spinner="Carregando e limpando dados...")
def _carregar_dados():
    """
    Baixa (se preciso) e limpa o dataset uma única vez; cacheia entre reruns.

    O @st.cache_data garante que:
      - A ingestão roda apenas na primeira carga da página.
      - Mudanças nos filtros NÃO disparam re-ingestão (só re-renderização).
    """
    caminho = garantir_dataset_local()
    return clean_sales_data(caminho, fill_strategy="median")


def iniciar_dashboard_view() -> None:
    """
    Orquestra o dashboard web:
      1. Configura a página (DEVE ser a primeira chamada Streamlit).
      2. Carrega os dados (cacheados).
      3. Delega toda a renderização ao streamlit_adapter.
    """
    # ⚠️ st.set_page_config DEVE vir antes de qualquer outro comando Streamlit
    st.set_page_config(
        page_title="Cafe Sales Analytics",
        page_icon="☕",
        layout="wide",
    )

    # Carrega dados (cacheado — executa 1x por sessão)
    df_limpo = _carregar_dados()

    # Delega TUDO para o adapter (filtros + KPIs + gráficos)
    renderizar_dashboard_web(df_limpo)


if __name__ == "__main__":
    iniciar_dashboard_view()
