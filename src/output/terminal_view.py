from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# instância do Console global no escopo deste módulo para gerenciar as impressões
console = Console()


def exibir_dashboard_terminal(metricas: Dict[str, Any], **filtros_aplicados: Any) -> None:
    """
    Recebe os resultados matemáticos e renderiza um dashboard no terminal.

    Parâmetros:
      - metricas (dict): Dicionário contendo os cálculos estatísticos processados.
      - **filtros_aplicados: Filtros informados na orquestração para exibir no cabeçalho.
    """
    # 1. Tratamento de Erros na Apresentação
    # Se o motor estatístico retornou uma chave de erro, avisa o usuário com mensagem formatada
    if "erro" in metricas:
        console.print(Panel(f"[bold red]Erro no Processamento:[/bold red] {metricas['erro']}", title="⚠️ Alerta"))
        return

    # 2. Cabeçalho Dinâmico do Dashboard
    # Título para os filtros aplicados
    console.print("\n")
    if filtros_aplicados:
        texto_filtros = ", ".join([f"[cyan]{k}[/cyan]={v}" for k, v in filtros_aplicados.items()])
        titulo_painel = f"📊 DASHBOARD DE MÉTRICAS (Filtros: {texto_filtros})"
    else:
        titulo_painel = "📊 DASHBOARD DE MÉTRICAS (Visão Geral da Empresa)"

    console.print(
        Panel("[bold green]Análise Estatística Concluída com Sucesso![/bold green]", title=titulo_painel, expand=False))

    # 3. Construção da Tabela Estruturada
    # Objeto tabela
    tabela = Table(title="Indicadores de Desempenho (KPIs)", title_style="italic bold magenta", show_header=True,
                   header_style="bold blue")

    # Colunas
    tabela.add_column("Métrica de Performance", justify="left", style="white")
    tabela.add_column("Valor Calculado", justify="right", style="bold green")

    # 4. Linhas com validações seguras usando .get()
    # Usamos o .get() para evitar erros caso alguma métrica opcional não tenha sido calculada
    if "faturamento_total" in metricas:
        valor_faturamento = f"$ {metricas['faturamento_total']:,.2f}"
        tabela.add_row("Faturamento Bruto Total", valor_faturamento)

    if "ticket_medio" in metricas:
        valor_ticket = f"$ {metricas['ticket_medio']:,.2f}"
        tabela.add_row("Ticket Médio por Transação", valor_ticket)

    if "total_itens_vendidos" in metricas:
        valor_itens = f"{metricas['total_itens_vendidos']:,} unidades"
        tabela.add_row("Volume de Itens Vendidos", valor_itens)

    # 5. Renderizando na tela do usuário
    console.print(tabela)
    console.print("\n[dim]✨ Execução concluída sem efeitos colaterais de escopo.[/dim]\n")

