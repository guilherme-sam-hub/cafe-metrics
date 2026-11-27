"""
Adapter de saída para o Terminal (CLI) usando Rich para renderização rica.
"""

from __future__ import annotations

from typing import Any
import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def _formatar_moeda(valor: float) -> str:
    """Formata float para moeda BRL (ex: R$ 1.234,56)."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def exibir_kpis_terminal(kpis: dict, filtros: dict | None = None) -> None:
    """Exibe KPIs em painel formatado com Rich."""
    console.print("\n")

    # Tratamento de erro
    if "erro" in kpis:
        console.print(Panel(f"[bold red]{kpis['erro']}[/bold red]", title="⚠️ Erro", border_style="red"))
        return

    # Cabeçalho com filtros
    if filtros:
        texto_filtros = ", ".join([f"[cyan]{k}[/cyan]=[yellow]{v}[/yellow]" for k, v in filtros.items()])
        titulo = f"📊 KPIs (Filtros: {texto_filtros})"
    else:
        titulo = "📊 KPIs Gerais"

    # Tabela de KPIs
    tabela = Table(title=titulo, title_style="bold magenta", show_header=True, header_style="bold blue")
    tabela.add_column("Métrica", style="white", justify="left")
    tabela.add_column("Valor", style="bold green", justify="right")

    tabela.add_row("💰 Faturamento Total", _formatar_moeda(kpis['faturamento_total']))
    tabela.add_row("🎫 Ticket Médio", _formatar_moeda(kpis['ticket_medio']))
    tabela.add_row("📦 Itens Vendidos", f"{kpis['total_itens_vendidos']:,} un")

    console.print(Panel(tabela, border_style="green"))
    console.print("\n")


def exibir_analise_temporal_terminal(df_temporal: pd.DataFrame) -> None:
    """Exibe análise temporal em tabela Rich."""
    console.print("\n")

    if df_temporal.empty:
        console.print(Panel("[yellow]Nenhum dado temporal disponível.[/yellow]", title="📈 Análise Temporal", border_style="yellow"))
        return

    tabela = Table(title="📈 Evolução Mensal do Faturamento", title_style="bold cyan", show_header=True, header_style="bold blue")
    tabela.add_column("Mês", style="white")
    tabela.add_column("Faturamento", style="bold green", justify="right")
    tabela.add_column("Variação %", style="bold yellow", justify="right")

    for _, row in df_temporal.iterrows():
        var_str = f"{row['variacao_pct']:+.2f}%" if row['variacao_pct'] != 0 else "—"
        tabela.add_row(row['mes'], _formatar_moeda(row['faturamento']), var_str)

    console.print(Panel(tabela, border_style="cyan"))
    console.print("\n")


def exibir_anomalias_terminal(df_anomalias: pd.DataFrame) -> None:
    """Exibe anomalias detectadas."""
    console.print("\n")

    if df_anomalias.empty:
        console.print(Panel("[green]✅ Nenhuma anomalia estatística detectada.[/green]", title="🚨 Anomalias (Z-Score > 2.0)", border_style="green"))
        return

    console.print(Panel(f"[bold red]{len(df_anomalias)} anomalia(s) detectada(s)[/bold red]", title="🚨 Anomalias", border_style="red"))

    tabela = Table(show_header=True, header_style="bold red")
    tabela.add_column("Mês", style="white")
    tabela.add_column("Faturamento", style="bold yellow", justify="right")
    tabela.add_column("Z-Score", style="bold red", justify="right")
    tabela.add_column("Direção", style="bold magenta")

    for _, row in df_anomalias.iterrows():
        direcao = "📈 ALTA" if row['z_score'] > 0 else "📉 BAIXA"
        tabela.add_row(row['mes'], _formatar_moeda(row['faturamento']), f"{row['z_score']:+.2f}", direcao)

    console.print(tabela)
    console.print("\n")


def exibir_busca_terminal(df_resultado: pd.DataFrame, chave: str, valor: str) -> None:
    """Exibe resultado de busca linear."""
    console.print("\n")

    if df_resultado.empty:
        console.print(Panel(f"[yellow]Nenhum registro encontrado para '{valor}'.[/yellow]", title=f"🔍 Busca: {chave}", border_style="yellow"))
        return

    console.print(Panel(f"[green]{len(df_resultado)} venda(s) encontrada(s)[/green]", title=f"🔍 Busca: {chave}='{valor}'", border_style="green"))

    # Mostra apenas 5 primeiros resultados
    df_exibicao = df_resultado.head(5)
    tabela = Table(show_header=True, header_style="bold blue")
    tabela.add_column("ID", style="white")
    tabela.add_column("Item", style="cyan")
    tabela.add_column("Qtd", style="bold green", justify="right")
    tabela.add_column("Total", style="bold yellow", justify="right")

    for _, row in df_exibicao.iterrows():
        tabela.add_row(
            str(row.get('Transaction_ID', 'N/A')),
            str(row.get('Item', 'N/A')),
            str(row.get('Quantity', 0)),
            _formatar_moeda(row.get('Total_Spent', 0))
        )

    console.print(tabela)
    if len(df_resultado) > 5:
        console.print(f"[dim]... e mais {len(df_resultado) - 5} resultado(s)[/dim]")
    console.print("\n")


def exibir_ranking_terminal(df_ranking: pd.DataFrame) -> None:
    """Exibe ranking de produtos mais vendidos."""
    console.print("\n")

    if df_ranking.empty:
        console.print(Panel("[yellow]Nenhum dado de vendas para gerar o ranking.[/yellow]", title="🏆 Ranking", border_style="yellow"))
        return

    tabela = Table(title="🏆 Top 10 Produtos Mais Vendidos", title_style="bold magenta", show_header=True, header_style="bold blue")
    tabela.add_column("#", style="bold white", justify="center")
    tabela.add_column("Produto", style="cyan")
    tabela.add_column("Total Vendido", style="bold green", justify="right")

    for i, (_, row) in enumerate(df_ranking.head(10).iterrows(), 1):
        medalha = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
        tabela.add_row(medalha, row['Item'], f"{row['Total_Vendido']:,} un")

    console.print(Panel(tabela, border_style="magenta"))
    console.print("\n")


def exibir_sucesso_salvamento(caminhos: list[str]) -> None:
    """Exibe mensagem de sucesso ao salvar gráficos."""
    console.print("\n")
    console.print(Panel(
        "[green]✅ Gráficos gerados com sucesso![/green]\n" +
        "\n".join([f"  📄 {c}" for c in caminhos]),
        title="🎨 Geração de Gráficos",
        border_style="green"
    ))
    console.print("\n")
