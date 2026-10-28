import shutil
from pathlib import Path
import kagglehub
from ..core import config


def garantir_dataset_local() -> Path:
    """
    Verifica se o arquivo CSV já existe na pasta data/.
    Se não existir, usa o kagglehub para baixar e mover para o escopo do projeto.

    Retorna:
        Path: O caminho local do arquivo bruto.
    """
    # Se o arquivo já estiver na pasta data/, não faz nada
    if config.RAW_DATA_PATH.exists():
        print(f"[INGESTÃO] Dataset já encontrado localmente em: {config.RAW_DATA_PATH}")
        return config.RAW_DATA_PATH

    print("[INGESTÃO] Dataset não encontrado. Iniciando download via kagglehub...")

    # Garante que a pasta 'data' existe no projeto antes de mover o arquivo
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)

    # O kagglehub baixa os arquivos em uma pasta cache global
    cache_path_str = kagglehub.dataset_download(config.KAGGLE_DATASET_ID)
    cache_dir = Path(cache_path_str)

    # Varre a pasta do cache procurando pelo arquivo .csv do Cafe Sales
    arquivos_csv = list(cache_dir.glob("*.csv"))

    if not arquivos_csv:
        raise FileNotFoundError("Download concluído, mas nenhum arquivo CSV foi encontrado no cache.")

    arquivo_baixado = arquivos_csv[0]

    # Move o arquivo da pasta de cache global para a pasta data/ do nosso projeto
    # com o nome exato mapeado no nosso config.py
    shutil.move(str(arquivo_baixado), str(config.RAW_DATA_PATH))
    print(f"[INGESTÃO] Dataset baixado e movido com sucesso para: {config.RAW_DATA_PATH}")

    return config.RAW_DATA_PATH