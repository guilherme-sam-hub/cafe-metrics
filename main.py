
from src.core import config
from src.ingestion import garantir_dataset_local, clean_sales_data
from src.analytics import calcular_metricas_vendas
from src.output import exibir_dashboard_terminal


def rodar_pipeline_sistema():
    """
    Função principal que orquestra o fluxo de dados do Monolito Modular.
    Controla o escopo de execução e conexões entre módulos.
    """
    # ETAPA 1: Garantir que o dado bruto existe (baixa se necessário)
    caminho_dados = garantir_dataset_local()

    # ETAPA 2: Ingestão e Sanitização (Limpando "ERROR", aplicando a estratégia de mediana)
    df_limpo = clean_sales_data(caminho_dados, fill_strategy="median")

    # --- EXEMPLO 1: Renderizando Visão Geral da Empresa ---
    # O motor calcula todas as métricas padrão por falta de argumentos em *args
    resultados_gerais = calcular_metricas_vendas(df_limpo)
    exibir_dashboard_terminal(resultados_gerais)

    # --- EXEMPLO 2: Análise Filtrada Dinamicamente com **kwargs ---
    # Simulando um filtro avançado: Queremos analisar apenas as vendas de "Coffee"
    filtros_cafe = {"Item": "Coffee"}

    # Desempacotamos o dicionário usando '**' para passar como kwargs dinâmicos
    resultados_cafe = calcular_metricas_vendas(df_limpo, **filtros_cafe)
    exibir_dashboard_terminal(resultados_cafe, **filtros_cafe)


# O bloco idiomático garante que o pipeline só rode se o arquivo for executado diretamente
if __name__ == "__main__":
    rodar_pipeline_sistema()
