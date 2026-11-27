"""
Módulo de limpeza e padronização do dataset de vendas de café.
Responsável por transformar dados brutos em dados analíticos.
"""

import pandas as pd
from pathlib import Path

from ..core import config


def clean_sales_data(file_path: Path | str, *, fill_strategy: str = "median") -> pd.DataFrame:
    """
    Lê o dataset bruto, aplica saneamento e retorna um DataFrame limpo.

    Args:
        file_path: Caminho para o CSV bruto.
        fill_strategy: 'median' ou 'mean' para preenchimento de preços.
    """
    print(f"[INGESTÃO] Iniciando limpeza do arquivo: {file_path}")

    if fill_strategy not in ("median", "mean"):
        raise ValueError(f"Estratégia '{fill_strategy}' inválida. Use 'median' ou 'mean'.")

    # 1. Leitura com saneamento antecipado (na_values)
    # O Pandas converte automaticamente os sinais de sujeira em NaN/NA durante a leitura
    df = pd.read_csv(file_path, na_values=config.DIRTY_SIGNALS)

    # 2. Normalização dos Nomes das Colunas
    # Remove espaços extras nas pontas e padroniza para snake_case
    df.columns = df.columns.str.strip().str.replace(" ", "_")

    # Mapeamento específico para colunas que mudam de nome (não só espaços)
    mapeamento_especifico = {
        "Transaction_ID": "Transaction_ID", # Mantém
        "Price_Per_Unit": "Price_Per_Item", # Kaggle às vezes varia entre Unit/Item
    }
    df = df.rename(columns=mapeamento_especifico)

    print(f"[INGESTÃO] Colunas padronizadas: {list(df.columns)}")

    # 3. Conversão e Preenchimento de Preços (Price_Per_Item)
    # Força numérico, o que já era texto sujo vira NaN
    df["Price_Per_Item"] = pd.to_numeric(df["Price_Per_Item"], errors="coerce")

    valor_preenchimento = df["Price_Per_Item"].median() if fill_strategy == "median" else df["Price_Per_Item"].mean()
    df["Price_Per_Item"] = df["Price_Per_Item"].fillna(valor_preenchimento).astype(float)

    # 4. Quantidade e Datas
    # Premissa de negócio: Se a quantidade é desconhecida, assumimos 1 unidade para não zerar a venda
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(1).astype(int)

    df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"], errors="coerce")
    # Regra de negócio: Vendas sem data são inúteis para análise temporal
    df = df.dropna(subset=["Transaction_Date"])

    # 5. Recálculo de Segurança (Total_Spent)
    # Garante que o total bate com a matemática (Qtd * Preço)
    df["Total_Spent"] = (df["Quantity"] * df["Price_Per_Item"]).round(2)

    # 6. Higienização de Strings (Categorização)
    # Item e Location: Capitalizados (Title Case)
    for col in ["Item", "Location"]:
        if col in df.columns:
            # Usa o tipo 'string' do pandas (suporta pd.NA nativamente)
            df[col] = df[col].astype("string").str.strip().str.title().fillna("Desconhecido")

    # Payment_Method: Maiúsculas
    if "Payment_Method" in df.columns:
        df["Payment_Method"] = (
            df["Payment_Method"]
            .astype("string")
            .str.strip()
            .str.upper()
            .fillna("DESCONHECIDO")
        )

    # 7. Persistência (bom para auditoria)
    config.CLEAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.CLEAN_DATA_PATH, index=False)
    print(f"[INGESTÃO] Dataset limpo salvo em: {config.CLEAN_DATA_PATH}")

    return df
