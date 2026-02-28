import pandas as pd
import random
from datetime import datetime, timedelta
import uuid

# Configurações
NUM_USERS = 5000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 1, 1)

plans = {
    "Basic": 29,
    "Pro": 59,
    "Enterprise": 99
}

countries = ["Brasil", "USA", "Canada", "Portugal", "Spain"]

# =========================
# 1. GERAR USERS
# =========================

users = []

for i in range(NUM_USERS):
    user_id = str(uuid.uuid4())
    created_at = START_DATE + timedelta(days=random.randint(0, 365))

    users.append({
        "user_id": user_id,
        "created_at": created_at,
        "country": random.choice(countries)
    })

    df_users = pd.DataFrame(users)

# =========================
# 2. GERAR SUBSCRIPTIONS
# =========================

subscriptions = []

for _, user in df_users.iterrows():
    subscription_id = str(uuid.uuid4())
    plan = random.choice(list(plans.keys()))
    start_date = user["created_at"]

    # 30% chance de churn
    if random.random() < 0.3:
        cancel_date = start_date + timedelta(days=random.randint(30, 365))
        status = "canceled"
    else:
        cancel_date = None
        status = "active"

    subscriptions.append({
        "subscription_id": subscription_id,
        "user_id": user["user_id"],
        "plan": plan,
        "start_date": start_date,
        "cancel_date": cancel_date,
        "monthly_value": plans[plan],
        "status": status
    })

    df_subscriptions = pd.DataFrame(subscriptions)

# =========================
# 3. GERAR PAYMENTS
# =========================

payments = []

for _, sub in df_subscriptions.iterrows():
    current_date = sub["start_date"]

    while True:
        if sub["cancel_date"] and current_date > sub["cancel_date"]:
            break
        if current_date > END_DATE:
            break

        payments.append({
            "payment_id": str(uuid.uuid4()),
            "subscription_id": sub["subscription_id"],
            "payment_date": current_date,
            "amount": sub["monthly_value"],
            "payment_status": "paid"
        })

        current_date += timedelta(days=30)

df_payments = pd.DataFrame(payments)

# =========================
# SALVAR (DATA LAKE SIMULADO)
# =========================

df_users.to_csv("data_users.csv", index=False)
df_subscriptions.to_csv("data_subscriptions.csv", index=False)
df_payments.to_csv("data_payments.csv", index=False)

print("Dados gerados com sucesso!")
print("Users:", len(df_users))
print("Subscriptions:", len(df_subscriptions))
print("Payments:", len(df_payments))