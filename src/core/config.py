from pathlib import Path #Classe para manipulação de arquivos e pastas

#1. DEFINIÇÃO DE DIRETÓRIOS

#1.1. Caminho absoluto
# a) (__file__) guarda o caminho deste arquivo
# b) .resolve transforma esse caminho em um caminho absoluto (completo)
# c) .parents[2] volta para a pasta raiz (ponto de referência fixo)
BASE_DIR = Path(__file__).resolve().parents[2]

#1.2. Caminhos para as pastas de dados brutos e exportação
DATA_DIR = BASE_DIR/"data"
EXPORTS_DIR = BASE_DIR/"exports"

#2. DEFINIÇÃO DOS ARQUIVOS ESPECÍFICOS
#2.1 Caminho para arquivo original
RAW_DATA_PATH = DATA_DIR/"cafe_sales_dirty.csv"

#2.2. caminho para o arquivo tratado
CLEAN_DATA_PATH = DATA_DIR/"cafe_sales_clean.csv"

#3. ESQUEMA E VALIDAÇÃO DE DADOS

#3.1. Contrato dos dados

EXPECTED_COLUMMS = {
    "Transaction_ID":int,
    "Item":str,
    "Quantity":int,
    "Price_Per_Item":float,

    "Total_Spent":float,
    "Payment_Method":str,

    "Location":str,

    "Transaction_Date":str,
}


#4. IDENTIFICAÇÃO DA "SUJEIRA DOS DADOS

#4.1. Para o script de limpeza encontrar e tratar os erros.
DIRTY_SIGNALS = ["ERROR", "UNKNOWN", "N/A", "NaN", "null"]

#5. CONFIGURAÇÃO DE DOWNLOAD (KAGGLE)

#5.1. Para baixar o dataset original via API do Kaggle
KAGGLE_DATASET_ID = "ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training"