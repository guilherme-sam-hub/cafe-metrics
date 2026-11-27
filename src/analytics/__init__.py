"""
Camada de análise (Core): KPIs, busca, ordenação, série temporal e anomalias.
Re-exporta as funções para facilitar o import no main.py e adapters.
"""

from .metricas import calcular_kpis
from .busca import busca_linear
from .ordenacao import ordenar_por_vendas
from .temporal import analise_temporal
from .anomalias import detectar_anomalias
from .estruturas import PilhaRelatorios

__all__ = [
    "calcular_kpis",
    "busca_linear",
    "ordenar_por_vendas",
    "analise_temporal",
    "detectar_anomalias",
    "PilhaRelatorios",
]
