import pandas as pd
from sqlalchemy import create_engine

# Conexão (ajuste usuário/senha)
engine = create_engine("postgresql://postgres:senha@localhost:5432/saas_analytics")

# Ler CSVs
df_users = pd.read_csv("data_users.csv")
df_subscriptions = pd.read_csv("data_subscriptions.csv")
df_payments = pd.read_csv("data_payments.csv")

# Carregar
df_users.to_sql("users", engine, schema="raw", if_exists="append", index=False)
df_subscriptions.to_sql("subscriptions", engine, schema="raw", if_exists="append", index=False)
df_payments.to_sql("payments", engine, schema="raw", if_exists="append", index=False)

print("Dados carregados com sucesso!")