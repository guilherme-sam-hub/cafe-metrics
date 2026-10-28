# src/ingestion/cleaners.py
import pandas as pd
from ..core import config


def clean_sales_data(file_path: str, *, fill_strategy: str = "median") -> pd.DataFrame:
    """
    Lê o dataset de vendas do café, traduz as colunas do Kaggle para o padrão do sistema
    e realiza a sanitização completa dos dados corrompidos.
    """
    print(f"[INGESTÃO] Iniciando leitura do arquivo: {file_path}")

    # 1. Leitura inicial dos dados
    df = pd.read_csv(file_path)

    # 2. Normalização e Limpeza Física dos Nomes das Colunas
    df.columns = df.columns.str.strip()

    # Mapeamento dinâmico: traduz o layout do Kaggle para o layout padrão com underlines do sistema
    mapeamento_colunas = {
        "Transaction ID": "Transaction_ID",
        "Item": "Item",
        "Quantity": "Quantity",
        "Price Per Unit": "Price_Per_Item",
        "Price Per Item": "Price_Per_Item",
        "Total Spent": "Total_Spent",
        "Payment Method": "Payment_Method",
        "Location": "Location",
        "Transaction Date": "Transaction_Date"
    }

    # Aplica a renomeação com base no dicionário de mapeamento
    df.rename(columns=mapeamento_colunas, inplace=True)

    # Substitui eventuais espaços remanescentes por underline para garantir consistência
    df.columns = df.columns.str.replace(" ", "_")

    print(f"[INGESTÃO] Colunas padronizadas internamente para: {list(df.columns)}")

    # 3. Varrendo o escopo do DataFrame atrás das strings sujas mapeadas no Core ("ERROR", "UNKNOWN")
    for signal in config.DIRTY_SIGNALS:
        df.replace(signal, pd.NA, inplace=True)

    # 4. Tratamento dos Valores Nulos Numéricos (Price_An_Item) usando Parâmetros Avançados
    if fill_strategy == "median":
        mediana_preco = pd.to_numeric(df["Price_Per_Item"], errors='coerce').median()
        df["Price_Per_Item"] = df["Price_Per_Item"].fillna(mediana_preco)
    elif fill_strategy == "mean":
        media_preco = pd.to_numeric(df["Price_Per_Item"], errors='coerce').mean()
        df["Price_Per_Item"] = df["Price_Per_Item"].fillna(media_preco)
    else:
        raise ValueError(f"Estratégia '{fill_strategy}' não é suportada. Use 'median' ou 'mean'.")

    # 5. Conversão Forçada de Tipos (Robustez de Tipagem)
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(1).astype(int)
    df["Price_Per_Item"] = pd.to_numeric(df["Price_Per_Item"], errors="coerce").astype(float)
    df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"], errors="coerce")

    # 6. Recálculo da Regra de Negócio Afetada pela Limpeza
    # Como corrigimos preços nulos/erros, o Total_Spent original precisa ser recalculado com precisão
    df["Total_Spent"] = df["Quantity"] * df["Price_Per_Item"]

    # 7. Higienização de Textos (Strings) para Agrupamentos Uniformes no Analytics
    df["Item"] = df["Item"].astype(str).str.strip().str.title()
    df["Payment_Method"] = df["Payment_Method"].astype(str).str.strip().str.upper()
    df["Location"] = df["Location"].astype(str).str.strip().str.title()

    # 8. Salvamento do Dataset Sanitizado para Auditoria Externa
    config.CLEAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.CLEAN_DATA_PATH, index=False)

    print("[INGESTÃO] Dados limpos, padronizados e persistidos com sucesso!")
    return df
