import pandas as pd
# Importação relativa: voltamos um nível e entramos em core.config
from ..core import config


def clean_sales_data(file_path: str, *, fill_strategy: str = "median") -> pd.DataFrame:
    """
    Lê o dataset de vendas do café e realiza a sanitização dos dados.

    Parâmetros:
      - file_path (str): O caminho do arquivo CSV bruto.
      - * (operador): Garante que todos os parâmetros seguintes SEJAM nomeados obrigatoriamente.
      - fill_strategy (str): Estratégia para tratar valores nulos numéricos ('median' ou 'mean').
    """
    print(f"[INGESTÃO] Iniciando leitura do arquivo: {file_path}")

    # 1. Leitura inicial dos dados
    df = pd.read_csv(file_path)

    # 2. Varrendo o escopo do DataFrame atrás das strings sujas mapeadas no Core
    # Substituímos termos como "ERROR" ou "UNKNOWN" por valores nulos reais do Pandas (NaN)
    for signal in config.DIRTY_SIGNALS:
        df.replace(signal, pd.NA, inplace=True)

    # 3. Aplicando os Parâmetros Avançados (Tomada de decisão arquitetural)
    # Dependendo do que o usuário escolheu via parâmetro nomeado, agimos de uma forma:
    if fill_strategy == "median":
        # Calcula a mediana (ignora erros) e preenche onde estava vazio
        mediana_preco = pd.to_numeric(df["Price_Per_Item"], errors='coerce').median()
        df["Price_Per_Item"] = df["Price_Per_Item"].fillna(mediana_preco)
    elif fill_strategy == "mean":
        # Calcula a média e preenche onde estava vazio
        media_preco = pd.to_numeric(df["Price_Per_Item"], errors='coerce').mean()
        df["Price_Per_Item"] = df["Price_Per_Item"].fillna(media_preco)
    else:
        # Se o desenvolvedor passar uma estratégia inválida, levantamos um erro de escopo
        raise ValueError(f"Estratégia '{fill_strategy}' não é suportada. Use 'median' ou 'mean'.")

    # O restante da sua lógica de tipagem e limpeza entra aqui...

    print("[INGESTÃO] Dados limpos com sucesso!")
    return df
