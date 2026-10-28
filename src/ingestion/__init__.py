from .loaders import garantir_dataset_local
from .cleaners import clean_sales_data

# O __all__ define o que será exportado quando alguém der 'from src.ingestion import *'
__all__ = ["garantir_dataset_local", "clean_sales_data"]
