"""
Módulo responsável por garantir a disponibilidade dos dados brutos.
Implementa uma estratégia de fallback: Local -> Amostra -> Download (Kaggle).
"""

import shutil
from pathlib import Path

from ..core import config


def garantir_dataset_local() -> Path:
    """
    Garante que o arquivo CSV bruto esteja disponível localmente.

    Ordem de prioridade:
      1. Dataset real (RAW_DATA_PATH)
      2. Amostra versionada (SAMPLE_DATA_PATH) — permite rodar sem Kaggle
      3. Download via kagglehub (último recurso)

    Retorna:
        Path: o caminho local do arquivo bruto garantido.

    Levanta:
        RuntimeError: se o download falhar ou o CSV baixado for inválido.
    """
    # 1. Dataset real presente?
    if config.RAW_DATA_PATH.exists():
        print(f"[INGESTÃO] Dataset já encontrado localmente em: {config.RAW_DATA_PATH}")
        return config.RAW_DATA_PATH

    # 2. Amostra versionada disponível?
    if config.SAMPLE_DATA_PATH.exists():
        print(
            f"[INGESTÃO] Dataset real ausente. Usando amostra versionada: "
            f"{config.SAMPLE_DATA_PATH}"
        )
        return config.SAMPLE_DATA_PATH

    # 3. Último recurso: baixar do Kaggle
    print("[INGESTÃO] Dataset e amostra não encontrados. Iniciando download via kagglehub...")

    # Import tardio: só carrega kagglehub se realmente precisar baixar
    import kagglehub

    try:
        cache_path_str = kagglehub.dataset_download(config.KAGGLE_DATASET_ID)
    except Exception as exc:
        raise RuntimeError(
            "Não foi possível baixar o dataset do Kaggle.\n"
            "Verifique:\n"
            "  - conexão com a internet\n"
            "  - credenciais em ~/.kaggle/kaggle.json\n"
            f"  - id do dataset em config.py: '{config.KAGGLE_DATASET_ID}'\n"
            f"Causa original: {exc}"
        ) from exc

    cache_dir = Path(cache_path_str)
    arquivos_csv = sorted(cache_dir.glob("*.csv"))

    if not arquivos_csv:
        raise FileNotFoundError(
            f"Download concluído, mas nenhum CSV encontrado em {cache_dir}."
        )

    # Heurística: o maior CSV costuma ser o dataset principal.
    arquivo_baixado = max(arquivos_csv, key=lambda p: p.stat().st_size)
    if len(arquivos_csv) > 1:
        print(
            f"[INGESTÃO] {len(arquivos_csv)} CSVs no cache; usando o maior: "
            f"{arquivo_baixado.name}"
        )

    # Copia (não move) — preserva o cache do kagglehub.
    # shutil.copy2 aceita Path objects diretamente (Python 3.6+)
    config.RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(arquivo_baixado, config.RAW_DATA_PATH)

    # Valida tamanho mínimo para não propagar CSV truncado.
    tamanho_arquivo = config.RAW_DATA_PATH.stat().st_size
    if tamanho_arquivo < 1024:  # 1KB é um limite seguro para um CSV de dados
        config.RAW_DATA_PATH.unlink(missing_ok=True)
        raise RuntimeError(
            f"CSV baixado parece inválido ({tamanho_arquivo} bytes). "
            f"Arquivo corrompido removido; tente novamente."
        )

    print(f"[INGESTÃO] Dataset copiado com sucesso para: {config.RAW_DATA_PATH}")
    return config.RAW_DATA_PATH
