from src.ingestion import garantir_dataset_local, clean_sales_data
from src.output import renderizar_dashboard_web


def iniciar_dashboard_view():
    # 1. Garante os dados físicos locais
    caminho_dados = garantir_dataset_local()

    # 2. Executa a limpeza e padronização
    df_limpo = clean_sales_data(caminho_dados, fill_strategy="median")

    # 3. Chama a nossa nova interface do Streamlit passando os dados limpos
    renderizar_dashboard_web(df_limpo)


if __name__ == "__main__":
    iniciar_dashboard_view()
