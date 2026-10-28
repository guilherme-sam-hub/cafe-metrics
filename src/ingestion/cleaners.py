import pandas as pd
# Importação relativa: volta um nível e entra em core.config
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
    # Substituição de termos como "ERROR" ou "UNKNOWN" por valores nulos reais do Pandas (NaN)
    for signal in config.DIRTY_SIGNALS:
        df.replace(signal, pd.NA, inplace=True)

    # 3. Aplicando Parâmetros Avançados
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

    # 4. CONVERSÃO FORÇADA DE TIPOS (Tipagem e Robustez)
    # conversão colunas numéricas forçando erros a virarem NaN para não quebrar o sistema
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(1).astype(int)
    df["Price_Per_Item"] = pd.to_numeric(df["Price_Per_Item"], errors="coerce").astype(float)

    # Tratando as datas para o formato padrão do Pandas
    df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"], errors="coerce")

    # 5. RECALCULANDO REGRAS DE NEGÓCIO AFETADAS PELA LIMPEZA
    # Recalcular para garantir consistência no módulo Analytics.
    df["Total_Spent"] = df["Quantity"] * df["Price_Per_Item"]

    # 6. HIGIENIZAÇÃO DE TEXTOS (Strings)
    # Remove espaços em branco extras e padroniza textos para evitar que "Coffee " e "Coffee" sejam contados separados
    df["Item"] = df["Item"].astype(str).str.strip().str.title()
    df["Payment_Method"] = df["Payment_Method"].astype(str).str.strip().str.upper()
    df["Location"] = df["Location"].astype(str).str.strip().str.title()

    # 7. SALVAR DATASET TRATADO
    # Salva uma cópia limpa na pasta de dados para fins de histórico
    config.CLEAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.CLEAN_DATA_PATH, index=False)

    print("[INGESTÃO] Dados limpos com sucesso!")
    return df
