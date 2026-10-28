# Cafe Sales: Monolito Modular Python ☕🐍

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP%208-green?style=for-the-badge)](https://peps.python.org/pep-0008/)
[![Architecture](https://img.shields.io/badge/Architecture-Monolith%20Modular-orange?style=for-the-badge)](https://pt.wikipedia.org/wiki/Arquitetura_de_software)

Este projeto implementa um **Monolito Modular em Python Puro** para ingestão, sanitização automatizada e análise estatística de métricas de desempenho de vendas. O sistema consome o dataset real do Kaggle *Cafe Sales: Dirty Data for Cleaning Training* e serve como base arquitetural e prova de conceito (PoC) para a futura construção de um **Mapa de Métricas Integrado**.

O objetivo principal deste repositório é demonstrar o domínio de **boas práticas de engenharia de software, separação de responsabilidades (SoC), contratos de código previsíveis e manipulação avançada de escopos em Python**, indo além dos tradicionais scripts lineares de análise de dados.

---

## 🏗️ Design Arquitetural & Estrutura de Pastas

Diferente de abordagens baseadas em Jupyter Notebooks, o sistema adota uma divisão rígida de camadas em scripts puros (`.py`), garantindo acoplamento fraco e alta coesão:

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
│   │   ├── cleaners.py             # Tratamento de ruídos ("ERROR", "UNKNOWN") e tipagem
│   │   └── loaders.py              # Integração de rede com a API do Kaggle
│   │
│   ├── analytics/                  # MÓDULO 2: Motor Estatístico (Domínio de Negócio)
│   │   ├── __init__.py             # Fachada do pacote (Facade Pattern)
│   │   └── statistics.py           # Agregações matemáticas puras e filtros dinâmicos
│   │
│   └── output/                     # MÓDULO 3: Apresentação e Visualização
│       ├── __init__.py             # Fachada do pacote (Facade Pattern)
│       └── terminal_view.py        # Interface CLI rica construída com a biblioteca Rich
│
├── main.py                         # Ponto de entrada (Bootstrapper do Pipeline)
├── requirements.txt                # Dependências gerenciadas do ecossistema
└── README.md                       # Documentação técnica
```

---

## 🛠️ Conceitos Avançados de Python Aplicados

### 1. Separação de Responsabilidades (SoC) & Facade Pattern
Cada subpasta dentro de `src` encapsula seu próprio domínio. O uso estratégico dos arquivos `__init__.py` expõe apenas as funções necessárias para a superfície através do atributo `__all__`. Isso permite que o arquivo `main.py` consuma o sistema de forma limpa e elegante:
```python
from src.ingestion import garantir_dataset_local, clean_sales_data
from src.analytics import calcular_metricas_vendas
from src.output import exibir_dashboard_terminal
```

### 2. Contratos Previsíveis com Keyword-Only Arguments (`*`)
No módulo de limpeza (`cleaners.py`), a assinatura da função força o desenvolvedor a nomear argumentos de decisão arquitetural, impedindo passagens acidentais por posição:
```python
def clean_sales_data(file_path: str, *, fill_strategy: str = "median") -> pd.DataFrame:
```

### 3. Filtros Altamente Flexíveis com `*args` e `**kwargs`
O motor estatístico (`statistics.py`) utiliza o desempacotamento dinâmico para aceitar qualquer combinação de filtros baseados nas colunas do dataset sem precisar alterar sua assinatura interna, garantindo a extensibilidade do código:
```python
def calcular_metricas_vendas(df: pd.DataFrame, *metricas_desejadas: str, **filtros: Any) -> Dict[str, Any]:
```

### 4. Isolamento de Escopo e Imutabilidade Contextual
Constantes de infraestrutura e strings de erro do Kaggle (`["ERROR", "UNKNOWN", "N/A"]`) são injetadas a partir de `src.core.config.py`, atuando como variáveis imutáveis no escopo global da aplicação.

---

## 📊 O Pipeline de Execução (Data Flow)

Quando o arquivo `main.py` é iniciado, o sistema executa os seguintes passos ordenadamente:

1. **`loaders.garantir_dataset_local()`**: Verifica o ambiente local. Se o arquivo não existir, conecta-se à API do Kaggle, baixa o dataset para o cache global do sistema e o move para a pasta `./data/`.
2. **`cleaners.clean_sales_data()`**: Caça os sinais de dados sujos, substitui-os usando a estratégia matemática escolhida (`mean` ou `median`), força a tipagem correta de cada coluna (`datetime`, `int`, `float`) e recalcula a coluna `Total_Spent` para manter a integridade fiscal.
3. **`statistics.calcular_metricas_vendas()`**: Isola e filtra o DataFrame dinamicamente e computa os indicadores de performance (KPIs).
4. **`terminal_view.exibir_dashboard_terminal()`**: Constrói componentes visuais estilizados (painéis e tabelas) renderizados diretamente no terminal do usuário.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.10 ou superior instalado.
* Uma conta no Kaggle (opcional, para download automático se o arquivo csv não for inserido manualmente).

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   cd cafe-metrics-monolith
   ```

2. **Crie e ative o ambiente virtual (Virtualenv):**
   ```bash
   python -m venv .venv
   # No Linux/Mac:
   source .venv/bin/activate
   # No Windows (Prompt de Comando):
   .venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   ```bash
   python main.py
   ```

---

## 🔮 Próximos Passos (Evolução da Arquitetura)

Este monolito modular foi desenhado seguindo princípios de **DDD (Domain-Driven Design)** de forma simplificada. Devido ao isolamento rígido dos pacotes, o sistema está totalmente pronto para os seguintes próximos passos:
*   [ ] **Migração para Microsserviços**: Desacoplar o módulo `analytics` para um serviço independente exposto via FastAPI ou gRPC.
*   [ ] **Expansão da Camada de Apresentação**: Substituir o `terminal_view` por um frontend web interativo para dar vida ao **Mapa de Métricas Integrado**.
*   [ ] **Pipeline de Testes**: Implementação de testes unitários com `pytest` para garantir a idempotência do motor estatístico.

---
Desenvolvido por [guilherme-sam-hub]
