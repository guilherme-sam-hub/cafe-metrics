# Cafe Sales: Monolito Modular & Dashboard Interativo ☕🐍📊

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP%208-green?style=for-the-badge)](https://peps.python.org/pep-0008/)
[![Architecture](https://img.shields.io/badge/Architecture-Monolith%20Modular-orange?style=for-the-badge)](https://pt.wikipedia.org/wiki/Arquitetura_de_software)

Este projeto implementa um **Monolito Modular em Python Puro** para ingestão, sanitização automatizada e análise estatística de métricas de desempenho de vendas. O sistema consome o dataset real do Kaggle *Cafe Sales: Dirty Data for Cleaning Training* e serve como base arquitetural e prova de conceito (PoC) para a futura construção de um **Mapa de Métricas Integrado**.

A aplicação conta com **dois canais de apresentação desacoplados**: um painel rico via linha de comando (CLI) e um dashboard web totalmente interativo com gráficos responsivos.

---

## 🏗️ Design Arquitetural & Estrutura de Pastas

O sistema adota uma divisão rígida de camadas em scripts puros (`.py`), garantindo baixo acoplamento e alta coesão. Graças a essa arquitetura, a lógica de negócios é centralizada e compartilhada entre as interfaces de Terminal e Web:

```text
cafe_metrics/
│
├── data/                           # Repositório de dados (Ignorado no Git)
│   ├── cafe_sales_dirty.csv        # Dataset bruto baixado via API
│   └── cafe_sales_clean.csv        # Dataset persistido pós-sanitização
│
├── exports/                        # Saídas físicas do sistema (relatórios, imagens)
│
├── src/                            # Núcleo da Aplicação (O Monolito)
│   ├── __init__.py                 # Inicializador do pacote raiz
│   │
│   ├── core/                       # Camada de Configuração Global e Constantes
│   │   ├── __init__.py
│   │   └── config.py               # Single Source of Truth para caminhos e metadados
│   │
│   ├── ingestion/                  # MÓDULO 1: Orquestração e Higienização de Dados
│   │   ├── __init__.py             # Fachada do pacote (Facade Pattern)
│   │   ├── cleaners.py             # Mapeamento do Kaggle, tratamento de nulos e tipagem
│   │   └── loaders.py              # Integração de rede com a API do Kaggle
│   │
│   ├── analytics/                  # MÓDULO 2: Motor Estatístico (Domínio de Negócio)
│   │   ├── __init__.py             # Fachada do pacote (Facade Pattern)
│   │   └── statistics.py           # Agregações matemáticas puras e filtros dinâmicos
│   │
│   └── output/                     # MÓDULO 3: Apresentação e Visualização
│       ├── __init__.py             # Fachada do pacote (Facade Pattern)
│       ├── terminal_view.py        # Interface CLI rica construída com Rich
│       └── web_view.py             # Painel Web interativo com Streamlit e Plotly
│
├── main.py                         # Ponto de entrada 1: Bootstrapper do Painel Terminal
├── app_web.py                      # Ponto de entrada 2: Bootstrapper do Dashboard Web
├── requirements.txt                # Dependências gerenciadas do ecossistema
└── README.md                       # Documentação técnica
```

---

## 🛠️ Conceitos Avançados de Python Aplicados

### 1. Separação de Responsabilidades (SoC) & Facade Pattern
Cada subpasta dentro de `src` encapsula seu próprio domínio. O uso estratégico dos arquivos `__init__.py` expõe apenas as funções necessárias para a superfície através do atributo `__all__`. Isso permite que o sistema mude de interface sem tocar na lógica de higienização de dados.

### 2. Contratos Previsíveis com Keyword-Only Arguments (`*`)
No módulo de limpeza (`cleaners.py`), a assinatura da função força o desenvolvedor a nomear argumentos de decisão arquitetural, impedindo passagens acidentais por posição:
```python
def clean_sales_data(file_path: str, *, fill_strategy: str = "median") -> pd.DataFrame:
```

### 3. Filtros Dinâmicos com `**kwargs` e Desempacotamento
O motor estatístico (`statistics.py`) utiliza o desempacotamento dinâmico para aceitar qualquer combinação de filtros baseados nas colunas do dataset. Esses filtros são mapeados diretamente a partir dos seletores visuais do Streamlit ou parâmetros de linha de comando:
```python
def calcular_metricas_vendas(df: pd.DataFrame, *metricas_desejadas: str, **filtros: Any) -> Dict[str, Any]:
```

### 4. Resolução de Divergência de Esquemas (Data Schema Mapping)
O pipeline conta com uma camada defensiva que captura o cabeçalho original do Kaggle (`Price Per Unit`) e o traduz imediatamente para o contrato interno padronizado do sistema (`Price_Per_Item`), blindando o motor analítico contra quebras de layout externo.

---

## 📊 O Pipeline de Execução (Data Flow)

Quando qualquer um dos pontos de entrada (`main.py` ou `app_web.py`) é iniciado, o sistema executa os seguintes passos ordenadamente:

1. **`loaders.garantir_dataset_local()`**: Verifica o ambiente local. Se o arquivo não existir, conecta-se à API do Kaggle via `kagglehub` e baixa os dados.
2. **`cleaners.clean_sales_data()`**: Remove os sinais de dados sujos (`"ERROR"`, `"UNKNOWN"`), aplica a estratégia matemática (`mean` ou `median`), força a tipagem correta de cada coluna e recalcula o `Total_Spent`.
3. **`statistics.calcular_metricas_vendas()`**: Isola e filtra o DataFrame dinamicamente através de dicionários desempacotados.
4. **`output` (Apresentação)**: Renderiza os dados no canal escolhido pelo usuário (Console ou Navegador).

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.10 ou superior instalado.
* Ambiente virtual configurado e ativo.

### Passo a Passo

1. **Clone o repositório e acesse a pasta:**
   ```bash
   git clone https://github.com
   cd cafe-metrics
   ```

2. **Crie e ative o ambiente virtual (Virtualenv):**
   ```bash
   python -m venv .venv
   # No Linux/Mac:
   source .venv/bin/activate
   # No Windows (Prompt de Comando):
   .venv\Scripts\activate
   ```

3. **Instale todas as dependências do ecossistema:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execução Canal 1 - Dashboard no Terminal (CLI):**
   ```bash
   python main.py
   ```

5. **Execução Canal 2 - Dashboard Interativo na Web (Streamlit):**
   ```bash
   streamlit run app_web.py
   ```

---

## 🔮 Próximos Passos (Evolução da Arquitetura)

Este monolito modular foi desenhado seguindo princípios de **DDD (Domain-Driven Design)** de forma simplificada. Devido ao isolamento rígido dos pacotes, o sistema está totalmente pronto para os seguintes próximos passos:
*   [ ] **Migração para Microsserviços**: Desacoplar o módulo `analytics` para um microsserviço independente exposto via FastAPI ou gRPC.
*   [ ] **Testes de Regressão**: Implementação de testes unitários com `pytest` para validar a idempotência da limpeza de dados.

---

Desenvolvido por [guilherme-sam-hub]
