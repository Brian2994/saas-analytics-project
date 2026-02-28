# **SaaS Analytics Project**

## Objetivo
Construir um pipeline de dados completo para uma empresa SaaS fictícia de assinaturas, permitindo:
- Cálculo de MRR
- Cálculo de Churn
- Cálculo de LTV
- Modelagem analítica (Star Schema)
- Separação entre camadas RAW e analytics
- Simulação de ambiente real de engenharia de dados

## Arquitetura do Projeto

### Fluxo de dados:

```
Gerador Python -> CSV (Data Lake Simulado) -> PostgreSQL (RAW) -> Camada Analytics (Star Schema) -> Métricas (MRR, Churn, LTV)
```

## Estrutura do Projeto

```
saas-analytics-project/
│
├── data_users.csv
├── data_subscriptions.csv
├── data_payments.csv
│
├── scripts/
│   ├── generate_data.py
│   ├── load_to_postgres.py
│
├── sql/
│   ├── create_schemas.sql
│   ├── create_raw_tables.sql
│   ├── star_schema.sql
│   ├── mrr.sql
│   ├── churn.sql
│   ├── ltv.sql
│
├── requirements.txt
└── README.md
```

## Geração de Dados (Data Simulation)

Arquivo: generate_data.py

O que foi feito
- Geração de 5000 usuários
- Criação de assinaturas com planos:
    - Basic
    - Pro
    - Enterprise
- Simulação de churn (30% probabilidade)
- Geração de pagamentos mensais recorrentes
- Exportação para CSV

## Tabelas Geradas

**users:**
|coluna|descrição|
|--|--|
|user_id|UUID do usuário|
|created_at|data de criação|
|country|país|

**subscriptions:**
|coluna|descrição|
|--|--|
|subscription_id|UUID|
|user_id|FK|
|plan|plano|
|start_date|início|
|cancel_date|cancelamento|
|monthly_value|valor|
|status|ativo/cancelado|

**payments:**
|coluna|descrição|
|--|--|
|payment_id|UUID|
|subscription_id|FK|
|payment_date|data do pagamento|
|amount|valor|
|payment_status|status|

## Banco de dados

Banco: saas_analytics

Schemas:
`CREATE SCHEMA raw;`
`CREATE SCHEMA analytics;`

Separação professional:
- raw -> dados brutos
- analytics -> dados transformados

## Carga para PostgreSQL

Arquivo: load_to_postgres.py

Responsável por:
- Ler CSVs
- Inserir nas tabelas RAW
- Utilizar SQLAlchemy + psycopg2

### *Instalação das dependências*

Execute o comando: `pip install -r requirements.txt`

## Modelagem Analítica (Star Schema)

Granularidade da fato:
1 linha = 1 pagamento

### Fato Principal

analytics.fact_payments
contém:
- payment_id
- subscription_id
- user_id
- payment_date
- amount
- plan
- country

Criada via JOIN entre:
- raw.payments
- raw.subscriptions
- raw.users

### Dimensão de Data

analytics.dim_date
Campos:
- date
- year
- month
- year_month

## Métricas Implementadas

### MRR (Monthly Recurring Revenue)

```
SELECT
    DATE_TRUNC('month', payment_date) AS month,
    SUM(amount) AS mrr
FROM analytics.fact_payments
GROUP BY 1
ORDER BY 1;
```

### Churn Rate Mensal

Definição:
Cancelamentos no mês / Clientes ativos no início do mês

Implementado com:
- CTE
- generate_series
- Tratamento de divisão por zero

Lógica:
1. Calcular ativos no início do mês
2. Calcular cancelamentos no mês
3. Dividir

## LTV (Lifetime Value)

### LTV Histórico por Usuário:
```
SELECT
    user_id,
    SUM(amount) AS lifetime_revenue
FROM analytics.fact_payments
GROUP BY user_id;
```

### LTV Médio:
```
SELECT
    ROUND(AVG(lifetime_revenue), 2) AS avg_ltv
FROM (
    SELECT
        user_id,
        SUM(amount) AS lifetime_revenue
    FROM analytics.fact_payments
    GROUP BY user_id
) t;
```

### LTV por Plano
Permite análise estratégica de monetização.

## Conceitos Demonstrados

Este projeto demonstra:
- Construção de pipeline do zero
- Separação de camadas (raw vs analytics)
- Modelagem Star Schema
- SQL avançado (CTE, agregações, date_trunc)
- Métricas SaaS reais
- Pensamento analítico de negócio
- Estrutura profissional de projeto

## Proximos Passos (Evolução do Projeto)
- Implementar carga incremental
- Orquestra com Airflow
- Criar dashboard (Power BI ou Metabase)