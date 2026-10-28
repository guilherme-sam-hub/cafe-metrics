import pandas as pd
from typing import Tuple, Dict, Any


# 1. FUNÇÃO AUXILIAR DE ESCOPO LOCAL (Filtro Dinâmico)
def _aplicar_filtros_dinamicos(df: pd.DataFrame, **kwargs: Any) -> pd.DataFrame:
    """
    Função interna (indicada pelo '_') para filtrar o DataFrame.
    O **kwargs vai receber qualquer filtro passado no formato: coluna="valor"
    """
    df_filtrado = df.copy()

    # kwargs funciona como um dicionário: key é o nome da coluna, value é o filtro
    for coluna, valor in kwargs.items():
        # Verifica se a coluna realmente existe no DataFrame para evitar erros
        if coluna in df_filtrado.columns:
            print(f"[ANALYTICS] Aplicando filtro: {coluna} == {valor}")
            df_filtrado = df_filtrado[df_filtrado[coluna] == valor]

    return df_filtrado


# 2. FUNÇÃO PRINCIPAL COM *ARGS E **KWARGS
def calcular_metricas_vendas(df: pd.DataFrame, *metricas_desejadas: str, **filtros: Any) -> Dict[str, Any]:
    """
    Calcula métricas estatísticas baseadas em filtros dinâmicos.

    Parâmetros:
      - df (pd.DataFrame): O DataFrame limpo vindo do módulo de ingestão.
      - *metricas_desejadas: Quais cálculos o usuário quer rodar (ex: 'faturamento', 'ticket_medio').
      - **filtros: Filtros dinâmicos de coluna (ex: Location="Downtown", Payment_Method="Cash").
    """
    print("[ANALYTICS] Iniciando processamento do motor estatístico...")

    # Primeiro, isola os dados aplicando os filtros que vieram no **kwargs (filtros)
    df_trabalho = _aplicar_filtros_dinamicos(df, **filtros)

    # Se o filtro for tão restrito que não sobrou nenhuma linha, evita divisões por zero
    if df_trabalho.empty:
        print("[ANALYTICS] Alerta: Nenhum dado corresponde aos filtros aplicados.")
        return {"erro": "Nenhum dado encontrado para os filtros informados."}

    # Criamos o dicionário que vai guardar os resultados finais
    resultados = {}

    # Se o usuário não passou nenhuma métrica específica no *args, calculamos todas por padrão
    if not metricas_desejadas:
        metricas_desejadas = ("faturamento", "ticket_medio", "total_itens")

    # 3. Processando o *args (Iterando sobre a tupla de métricas solicitadas)
    for metrica in metricas_desejadas:
        if metrica == "faturamento":
            # Calcula a soma da coluna Total_Spent
            resultados["faturamento_total"] = float(df_trabalho["Total_Spent"].sum())

        elif metrica == "ticket_medio":
            # Calcula a média aritmética das vendas
            resultados["ticket_medio"] = float(df_trabalho["Total_Spent"].mean())

        elif metrica == "total_itens":
            # Calcula a soma da quantidade de itens vendidos
            resultados["total_itens_vendidos"] = int(df_trabalho["Quantity"].sum())

    print("[ANALYTICS] Métricas calculadas com sucesso!")
    return resultados
