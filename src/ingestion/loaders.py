import shutil
from pathlib import Path
import kagglehub
from ..core import config

def garantir_dataset_local() -> Path:
    """
    Verifica se o arquivo CSV já existe na pasta data/.
    Ordem de prioridade:
      1. Dataset real (RAW_DATA_PATH)
      2. Dataset de amostra versionado (SAMPLE_DATA_PATH) — permite rodar sem Kaggle
      3. Download via kagglehub (último recurso)

    Retorna:
        Path: O caminho local do arquivo bruto.
    """
    # 1. Dataset real presente?
    if config.RAW_DATA_PATH.exists():
        print(f"[INGESTÃO] Dataset já encontrado localmente em: {config.RAW_DATA_PATH}")
        return config.RAW_DATA_PATH

    # 2. Amostra versionada disponível? (execução sem credenciais Kaggle)
    if config.SAMPLE_DATA_PATH.exists():
        print(f"[INGESTÃO] Dataset real ausente. Usando amostra versionada: {config.SAMPLE_DATA_PATH}")
        return config.SAMPLE_DATA_PATH

    # 3. Último recurso: baixar do Kaggle
    print("[INGESTÃO] Dataset e amostra não encontrados. Iniciando download via kagglehub...")

    config.DATA_DIR.mkdir(parents=True, exist_ok=True)

    cache_path_str = kagglehub.dataset_download(config.KAGGLE_DATASET_ID)
    cache_dir = Path(cache_path_str)

    arquivos_csv = list(cache_dir.glob("*.csv"))
    if not arquivos_csv:
        raise FileNotFoundError("Download concluído, mas nenhum arquivo CSV foi encontrado no cache.")

    arquivo_baixado = arquivos_csv[0]
    shutil.move(str(arquivo_baixado), str(config.RAW_DATA_PATH))
    print(f"[INGESTÃO] Dataset baixado e movido com sucesso para: {config.RAW_DATA_PATH}")

    return config.RAW_DATA_PATH