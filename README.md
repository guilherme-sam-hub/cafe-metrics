# ☕ Cafe Metrics — Arquitetura em Camadas & Dashboard Interativo

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP%208-green?style=for-the-badge)](https://peps.python.org/pep-0008/)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20Architecture-orange?style=for-the-badge)](https://pt.wikipedia.org/wiki/Arquitetura_de_software)
[![Tests](https://img.shields.io/badge/Tests-32%2F32%20passing-brightgreen?style=for-the-badge)](https://pytest.org/)
[![Coverage](https://img.shields.io/badge/Coverage-88%25%20Core-green?style=for-the-badge)](https://pytest-cov.readthedocs.io/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-purple?style=for-the-badge&logo=streamlit)](https://cafe-metrics-6qj2ynjj2e9mkx5vxv89sv.streamlit.app/)

Sistema analítico de vendas construído com **Clean Architecture** em Python puro. Ingestão automatizada, sanitização de dados sujos, motor estatístico agnóstico de UI e **dois canais de apresentação desacoplados** (CLI interativo e dashboard web).

🔗 **Dashboard ao vivo**: <https://cafe-metrics-6qj2ynjj2e9mkx5vxv89sv.streamlit.app/>

---

## 🎯 O Que Este Projeto Faz

- **Ingesta** dados brutos do Kaggle (*Cafe Sales: Dirty Data for Cleaning Training*) com *fallback strategy* (local → amostra → download)
- **Sanitiza** automaticamente sinais de sujeira (`ERROR`, `UNKNOWN`, `N/A`, `<NA>`, duplicatas)
- **Calcula** KPIs financeiros, série temporal com variação %, detecção de anomalias por Z-score, ranking de produtos e busca linear
- **Apresenta** os resultados via:
  - 🖥️ **CLI interativo** com menu, histórico de relatórios (pilha LIFO) e gráficos PNG
  - 🌐 **Dashboard web** com Streamlit + Plotly (filtros dinâmicos, gráficos responsivos)

---

## 🏗️ Arquitetura em Camadas

```text
┌─────────────────────────────────────────────────────────────┐
│                      ENTRY POINTS                           │
│     main.py (CLI)              app_web.py (Streamlit)       │
└──────────────┬──────────────────────────┬───────────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────────┐  ┌────────────────────────────┐
│   OUTPUT (Adapters)      │  │   OUTPUT (Adapters)        │
│   • cli_adapter (Rich)   │  │   • streamlit_adapter      │
│   • matplotlib_adapter   │  │   • (Plotly interativo)    │
└──────────────┬───────────┘  └──────────────┬─────────────┘
               │                              │
               └──────────────┬───────────────┘
                              ▼
              ┌───────────────────────────────┐
              │   ANALYTICS (Core Puro)       │
              │   • metricas • temporal       │
              │   • anomalias • busca         │
              │   • ordenacao • estruturas    │
              └───────────────┬───────────────┘
                              ▼
              ┌───────────────────────────────┐
              │   INGESTION (Dados)           │
              │   • loader (fallback)         │
              │   • cleaners (ETL)            │
              └───────────────┬───────────────┘
                              ▼
              ┌───────────────────────────────┐
              │   CORE (Config)               │
              └───────────────────────────────┘
              
## 🧩 Princípios Aplicados

| Princípio | Aplicação |
|-----------|-----------|
| **SRP** | Cada módulo tem uma responsabilidade única |
| **DRY** | Lógica de negócio existe em um único lugar (Core) |
| **Open/Closed** | Novo *entry point* sem modificar o Core |
| **Adapter Pattern** | CLI, Matplotlib e Streamlit são adapters independentes |
| **Command Pattern** | Menu CLI usa tabela de despacho (`ACOES`) |
| **Fail Fast** | Validações antecipadas em todas as funções |

---

## 📁 Estrutura do Projeto

```text
cafe-metrics/
│
├── data/                           # Dados brutos (Git-ignored, exceto amostra)
│   ├── .gitkeep
│   └── sample_dirty_cafe.csv       # Amostra versionada para deploy imediato
│
├── exports/                        # Saídas físicas (gráficos PNG, relatórios)
│
├── src/                            # Núcleo da Aplicação
│   ├── __init__.py
│   │
│   ├── core/                       # Camada 0: Configuração Global
│   │   ├── __init__.py
│   │   └── config.py               # Single Source of Truth (caminhos, schema, sinais)
│   │
│   ├── ingestion/                  # Camada 1: Ingestão e Higienização
│   │   ├── __init__.py             # Fachada do pacote
│   │   ├── loader.py               # Fallback Strategy (Local → Amostra → Kaggle)
│   │   └── cleaners.py             # ETL: mapeamento de schema, tipagem, nulos
│   │
│   ├── analytics/                  # Camada 2: Core de Negócio (agnóstico de UI)
│   │   ├── __init__.py             # Fachada do pacote (re-exporta funções públicas)
│   │   ├── metricas.py             # calcular_kpis() — KPIs financeiros
│   │   ├── temporal.py             # analise_temporal() — série temporal + variação %
│   │   ├── anomalias.py            # detectar_anomalias() — Z-score populacional (ddof=0)
│   │   ├── busca.py                # busca_linear() — filtro vetorizado
│   │   ├── ordenacao.py            # ordenar_por_vendas() — ranking agregado
│   │   └── estruturas.py           # PilhaRelatorios (LIFO para histórico)
│   │
│   └── output/                     # Camada 3: Adapters de Apresentação
│       ├── __init__.py             # Fachada do pacote
│       ├── cli_adapter.py          # Adapter Terminal (Rich: painéis, tabelas coloridas)
│       ├── matplotlib_adapter.py   # Adapter Estático (PNGs para relatórios/auditoria)
│       └── streamlit_adapter.py    # Adapter Web (Streamlit + Plotly interativo)
│
├── tests/                          # Suíte de testes unitários
│   ├── __init__.py
│   ├── conftest.py                 # Fixtures compartilhadas (DataFrames sintéticos)
│   ├── test_metricas.py
│   ├── test_temporal.py
│   ├── test_anomalias.py
│   ├── test_busca.py
│   ├── test_ordenacao.py
│   └── test_cleaners.py
│
├── main.py                         # Entry Point 1: Menu interativo CLI
├── app_web.py                      # Entry Point 2: Dashboard Streamlit
├── pytest.ini                      # Configuração do pytest
├── requirements.txt                # Dependências do ecossistema
└── README.md                       # Esta documentação
```

---

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.10 ou superior
- Git instalado
- (Opcional) Credenciais do Kaggle para o dataset completo

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/guilherme-sam-hub/cafe-metrics.git
cd cafe-metrics

# 2. Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate          # Linux/Mac
.venv\Scripts\activate             # Windows (PowerShell)

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o CLI interativo
python main.py

# 5. Execute o dashboard web
streamlit run app_web.py
```

---

## 🧪 Testes Unitários

O Core Analytics é **100% testável com DataFrames sintéticos** (sem I/O, sem rede).

```bash
# Instale o pytest-cov (se ainda não tiver)
pip install pytest-cov

# Rode todos os testes com cobertura
pytest --cov=src --cov-report=term-missing
```

### Cobertura Atual

| Módulo | Cobertura |
|--------|-----------|
| `src/analytics/metricas.py` | 100% |
| `src/analytics/temporal.py` | 100% |
| `src/analytics/busca.py` | 100% |
| `src/analytics/anomalias.py` | 92% |
| `src/analytics/ordenacao.py` | 86% |
| `src/ingestion/cleaners.py` | 100% |
| **Média do Core** | **~88%** |

---

## 📊 Dataset

O projeto usa o dataset [Cafe Sales: Dirty Data for Cleaning Training](https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training) do Kaggle.

### Fallback Strategy do Loader

1. `data/dirty_cafe_sales.csv` — dataset completo, se presente localmente
2. `data/sample_dirty_cafe.csv` — amostra versionada (padrão após o clone)
3. Download automático via `kagglehub` — requer credenciais do Kaggle

### Usando o Dataset Completo

**Opção A — Download manual:**

1. Baixe de <https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training>
2. Salve como `data/dirty_cafe_sales.csv`

**Opção B — Via API (requer credenciais):**

1. Gere um token em <https://www.kaggle.com/settings> → API
2. Configure as variáveis de ambiente:

```bash
export KAGGLE_USERNAME="seu_usuario"
export KAGGLE_KEY="sua_chave"
```

3. Remova `data/sample_dirty_cafe.csv` para forçar o download

---

## ☁️ Deploy no Streamlit Cloud

Este projeto está deployado e rodando ao vivo em:

👉 <https://cafe-metrics-6qj2ynjj2e9mkx5vxv89sv.streamlit.app/>

### Como Reproduzir o Deploy

1. Acesse <https://share.streamlit.io> e faça login com GitHub
2. Clique em **"New app"**
3. Configure:
   - **Repository**: `guilherme-sam-hub/cafe-metrics`
   - **Branch**: `main`
   - **Main file path**: `app_web.py`
4. (Opcional) Em **Advanced settings → Secrets**, adicione:

```toml
KAGGLE_USERNAME = "seu_usuario"
KAGGLE_KEY = "sua_chave"
```

---

## 🧠 Decisões Técnicas Notáveis

| Decisão | Justificativa |
|---------|---------------|
| `ddof=0` no desvio padrão | Trata a série temporal como população completa (não amostra) |
| `pct_change(fill_method=None)` | Evita `FutureWarning` do Pandas 2.2+ |
| `na_values=config.DIRTY_SIGNALS` no `read_csv` | Saneamento vetorizado em C — muito mais rápido que loop Python |
| `matplotlib.use("Agg")` no topo | Backend *headless* obrigatório para ambientes sem display (CI, servidores) |
| `plt.close(fig)` após cada `savefig` | Previne *memory leaks* na geração de múltiplos gráficos |
| `@st.cache_data` no `_carregar_dados()` | Garante que a ingestão rode apenas 1× por sessão Streamlit |
| Recálculo de `Total_Spent` | Garante integridade matemática (Qtd × Preço) mesmo se o CSV original tiver erro |
| `PilhaRelatorios` (LIFO) | Modela navegação "voltar" no CLI sem acoplar estado ao menu |

---

## 🔮 Próximos Passos

- Testes de integração para os adapters (mock de `rich.Console`, `st.plotly_chart`)
- Exportação de relatórios em PDF reutilizando `matplotlib_adapter.py` + `reportlab`
- Adapter de Telegram para envio diário de KPIs via bot
- CI/CD com GitHub Actions para rodar testes automaticamente a cada push
- Migração para **FastAPI** expondo o Core como microsserviço REST

---

## 📜 Licença & Créditos

- **Dataset original**: Ahmed Mohamed — [Cafe Sales: Dirty Data for Cleaning Training](https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training) (Kaggle, CC0).
- **Desenvolvido por**: [guilherme-sam-hub](https://github.com/guilherme-sam-hub)
