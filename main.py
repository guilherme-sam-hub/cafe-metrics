"""
Menu interativo do Mapa de Métricas — Cafe Sales (CLI).
Orquestrador principal da interface de terminal.
"""

from __future__ import annotations

from typing import Callable, Optional

import pandas as pd

from src.ingestion import garantir_dataset_local, clean_sales_data
from src.analytics import (
    calcular_kpis,
    analise_temporal,
    detectar_anomalias,
    busca_linear,
    ordenar_por_vendas,
    PilhaRelatorios,
)
from src.output.cli_adapter import (
    exibir_kpis_terminal,
    exibir_analise_temporal_terminal,
    exibir_anomalias_terminal,
    exibir_busca_terminal,
    exibir_ranking_terminal,
    exibir_sucesso_salvamento,
)
from src.output.matplotlib_adapter import gerar_e_salvar_graficos


# AÇÕES (Orquestradoras — delegam para Core + Adapter)

def _op_kpis(df: pd.DataFrame, hist: PilhaRelatorios) -> None:
    """KPIs gerais sem filtros."""
    resultado = calcular_kpis(df)
    exibir_kpis_terminal(resultado)
    hist.empilhar("KPIs gerais", resultado)


def _op_kpis_filtrados(df: pd.DataFrame, hist: PilhaRelatorios) -> None:
    """KPIs com filtros interativos."""
    filtros = _montar_filtros_interativos(df)
    if not filtros:
        print("⚠️  Nenhum filtro aplicado. Use a opção 1 para KPIs gerais.")
        return

    resultado = calcular_kpis(df, filtros=filtros)
    exibir_kpis_terminal(resultado, filtros=filtros)
    hist.empilhar(f"KPIs filtrados {filtros}", resultado)


def _montar_filtros_interativos(df: pd.DataFrame) -> dict:
    """Coleta filtros do usuário via terminal com numeração."""
    filtros: dict = {}

    for chave, rotulo in (("Item", "Produtos"), ("Location", "Locais")):
        opcoes = sorted(df[chave].dropna().astype(str).unique().tolist())
        if not opcoes:
            continue

        print(f"\n📋 {rotulo} disponíveis:")
        for i, op in enumerate(opcoes, 1):
            print(f"  {i}. {op}")

        bruto = input(f"Digite o número ({chave}) ou Enter p/ ignorar: ").strip()
        if bruto.isdigit():
            idx = int(bruto) - 1
            if 0 <= idx < len(opcoes):
                filtros[chave] = opcoes[idx]

    return filtros


def _op_busca(df: pd.DataFrame, hist: PilhaRelatorios) -> None:
    """Busca linear por produto."""
    item = input("🔍 Produto a buscar: ").strip().title()
    if not item:
        print("⚠️  Busca cancelada.")
        return

    # Nova busca_linear recebe DataFrame e retorna DataFrame
    achados = busca_linear(df, chave="Item", valor=item)
    exibir_busca_terminal(achados, chave="Item", valor=item)
    hist.empilhar(f"Busca: {item}", {"total": len(achados)})


def _op_temporal(df: pd.DataFrame, hist: PilhaRelatorios) -> None:
    """Análise temporal mês a mês."""
    df_temporal = analise_temporal(df)  # Retorna DataFrame direto
    exibir_analise_temporal_terminal(df_temporal)
    hist.empilhar("Análise temporal", df_temporal.to_dict("records"))


def _op_anomalias(df: pd.DataFrame, hist: PilhaRelatorios) -> None:
    """Detecção de anomalias por Z-score."""
    # Nova detectar_anomalias recebe DataFrame temporal direto
    df_temporal = analise_temporal(df)
    df_anomalias = detectar_anomalias(df_temporal)
    exibir_anomalias_terminal(df_anomalias)
    hist.empilhar("Anomalias detectadas", df_anomalias.to_dict("records"))


def _op_ordenar(df: pd.DataFrame, hist: PilhaRelatorios) -> None:
    """Ranking de produtos mais vendidos."""
    # Nova ordenar_por_vendas recebe DataFrame e retorna DataFrame
    df_ranking = ordenar_por_vendas(df)
    exibir_ranking_terminal(df_ranking)
    hist.empilhar("Ranking de vendas", df_ranking.to_dict("records"))


def _op_graficos(df: pd.DataFrame, hist: PilhaRelatorios) -> None:
    """Gera e salva gráficos PNG."""
    caminhos = gerar_e_salvar_graficos(df)
    exibir_sucesso_salvamento(caminhos)
    hist.empilhar("Geração de gráficos", {"arquivos": caminhos})


def _op_voltar(df: pd.DataFrame, hist: PilhaRelatorios) -> None:
    """Volta ao relatório anterior da pilha."""
    if hist.vazia():
        print("⚠️  Histórico vazio.")
        return

    titulo, resultado = hist.desempilhar()
    print(f"\n↩️  Voltando para: {titulo}")

    # Despacha para o adapter correto baseado no tipo do resultado
    if isinstance(resultado, dict):
        if "erro" in resultado:
            exibir_kpis_terminal(resultado)
        elif "faturamento_total" in resultado:
            exibir_kpis_terminal(resultado)
        elif "total" in resultado:
            print(f"  Total de registros: {resultado['total']}")
        elif "anomalias" in resultado:
            print(f"  Anomalias detectadas: {resultado['anomalias']}")
        elif "arquivos" in resultado:
            exibir_sucesso_salvamento(resultado["arquivos"])
    elif isinstance(resultado, list):
        # DataFrame convertido para records
        if resultado and "mes" in resultado[0]:
            df_temp = pd.DataFrame(resultado)
            exibir_analise_temporal_terminal(df_temp)
        elif resultado and "Item" in resultado[0]:
            df_rank = pd.DataFrame(resultado)
            exibir_ranking_terminal(df_rank)
        else:
            print(f"  Dados: {resultado[:3]}...")


def _op_historico(df: pd.DataFrame, hist: PilhaRelatorios) -> None:
    """Lista histórico de relatórios."""
    if hist.vazia():
        print("⚠️  Histórico vazio.")
        return

    print("\n📜 Histórico (mais recente primeiro):")
    for i, t in enumerate(hist.listar(), 1):
        print(f"  {i}. {t}")


# TABELA DE DESPACHO

ACOES: dict[str, tuple[str, Optional[Callable[[pd.DataFrame, PilhaRelatorios], None]]]] = {
    "1": ("KPIs gerais", _op_kpis),
    "2": ("KPIs filtrados (produto/filial)", _op_kpis_filtrados),
    "3": ("Buscar vendas de um produto", _op_busca),
    "4": ("Ranking de produtos mais vendidos", _op_ordenar),
    "5": ("Análise temporal", _op_temporal),
    "6": ("Detectar anomalias (Z-score)", _op_anomalias),
    "7": ("Gerar e salvar gráficos (.png)", _op_graficos),
    "8": ("Voltar ao relatório anterior", _op_voltar),
    "9": ("Listar histórico", _op_historico),
    "0": ("Sair", None),
}


# ENTRY POINT

def menu_interativo() -> None:
    """Loop principal do menu CLI."""
    print("\n[INGESTÃO] Carregando e limpando dados... aguarde.")

    try:
        caminho = garantir_dataset_local()
        df = clean_sales_data(caminho, fill_strategy="median")
        print("[INGESTÃO] ✅ Dados carregados com sucesso!\n")
    except Exception as e:
        print(f"[INGESTÃO] ❌ Erro fatal: {type(e).__name__}: {e}")
        return

    historico = PilhaRelatorios()

    try:
        while True:
            print("=" * 50)
            print("  📊 MAPA DE MÉTRICAS — CAFE SALES")
            print("=" * 50)
            for k, (desc, _) in ACOES.items():
                print(f"  [{k}] {desc}")
            print("=" * 50)

            escolha = input("\n👉 Escolha uma opção: ").strip()

            if escolha == "0":
                print("\n👋 Encerrando. Até logo!\n")
                break

            entrada = ACOES.get(escolha)
            if entrada is None or entrada[1] is None:
                print("❌ Opção inválida. Tente novamente.\n")
                continue

            try:
                entrada[1](df, historico)
            except Exception as e:
                print(f"❌ Erro na operação: {type(e).__name__}: {e}\n")

            print()  # Linha em branco para respirar

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Encerrando forçado. Até logo!\n")


if __name__ == "__main__":
    menu_interativo()
