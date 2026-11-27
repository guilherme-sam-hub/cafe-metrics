"""
Configurações globais e constantes do projeto Cafe Sales.
Centraliza caminhos, esquemas de dados e parâmetros de ingestão.
"""

from datetime import datetime
from pathlib import Path
import numpy as np  # Adicionado para tipagem correta do Pandas

# 1. DEFINIÇÃO DE DIRETÓRIOS

# 1.1. Caminho absoluto da raiz do projeto
# (__file__) -> src/core/config.py
# .parents[2] -> Sobe 3 níveis (core -> src -> raiz)
BASE_DIR = Path(__file__).resolve().parents[2]

# 1.2. Pastas principais
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"

# Garante que as pastas existam
DATA_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

# 2. DEFINIÇÃO DOS ARQUIVOS ESPECÍFICOS


RAW_DATA_PATH = DATA_DIR / "dirty_cafe_sales.csv"
SAMPLE_DATA_PATH = DATA_DIR / "sample_dirty_cafe.csv"
CLEAN_DATA_PATH = DATA_DIR / "cafe_sales_clean.csv"

# 3. ESQUEMA E VALIDAÇÃO DE DADOS

# Contrato de tipos esperado APÓS a limpeza (no DataFrame final).
# Nota: np.datetime64 para alinhar com o dtype nativo do Pandas.
EXPECTED_COLUMNS = {
    "Transaction_ID": int,
    "Item": str,
    "Quantity": int,
    "Price_Per_Item": float,
    "Total_Spent": float,
    "Payment_Method": str,
    "Location": str,
    "Transaction_Date": np.datetime64,
}

# 4. IDENTIFICAÇÃO DA "SUJEIRA" DOS DADOS

# Sinais que o cleaner deve converter em pd.NA / np.nan
DIRTY_SIGNALS = [
    "ERROR", "UNKNOWN", "N/A", "NA", "NaN", "Nan",
    "<Na>", "<NA>", "null", "Null", "NULL", "None", "none", ""
]

# 5. CONFIGURAÇÃO DE DOWNLOAD (KAGGLE)

KAGGLE_DATASET_ID = "ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training"
