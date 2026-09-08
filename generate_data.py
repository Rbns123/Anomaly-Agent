import pandas as pd
import numpy as np


# ============================================================
# 1. REPRODUCIBLE RANDOM DATA
# ============================================================

np.random.seed(42)


# ============================================================
# 2. BASIC SETTINGS
# ============================================================

DAYS = 365


# ============================================================
# 3. CREATE DAILY DATES
# ============================================================

dates = pd.date_range(
    start="2025-01-01",
    periods=DAYS,
    freq="D"
)


# ============================================================
# 4. NORMAL WEBSITE VISITORS
# ============================================================

visitors = np.random.normal(
    loc=12000,
    scale=1000,
    size=DAYS
).astype(int)

visitors = np.maximum(visitors, 1000)


# ============================================================
# 5. NORMAL CONVERSION RATE
# ============================================================

conversion_rate = np.random.normal(
    loc=4.2,
    scale=0.35,
    size=DAYS
)

conversion_rate = np.clip(
    conversion_rate,
    2.5,
    6.0
)


# ============================================================
# 6. CALCULATE ORDERS
# ============================================================

orders = (
    visitors * conversion_rate / 100
).astype(int)


# ============================================================
# 7. AVERAGE ORDER VALUE
# ============================================================

average_order_value = np.random.normal(
    loc=1000,
    scale=80,
    size=DAYS
)

average_order_value = np.maximum(
    average_order_value,
    500
)


# ============================================================
# 8. CALCULATE REVENUE
# ============================================================

revenue = orders * average_order_value


# ============================================================
# 9. NORMAL REFUNDS
# ============================================================

refunds = np.random.poisson(
    lam=25,
    size=DAYS
).astype(int)


# ============================================================
# 10. MARKETING SPEND
# ============================================================

marketing_spend = np.random.normal(
    loc=45000,
    scale=5000,
    size=DAYS
)

marketing_spend = np.maximum(
    marketing_spend,
    10000
)


# ============================================================
# 11. CREATE DATAFRAME
# ============================================================

df = pd.DataFrame({
    "date": dates,
    "visitors": visitors,
    "conversion_rate": conversion_rate,
    "orders": orders,
    "revenue": revenue,
    "refunds": refunds,
    "marketing_spend": marketing_spend
})


# ============================================================
# 12. GROUND-TRUTH ANOMALY LABELS
# ============================================================

df["is_anomaly"] = False
df["anomaly_type"] = "normal"


# ============================================================
# 13. ANOMALY 1 — TRAFFIC SPIKE
# ============================================================

traffic_date = "2025-01-31"

mask = df["date"] == traffic_date

df.loc[mask, "visitors"] = (
    df.loc[mask, "visitors"] * 2.8
).astype(int)

df.loc[mask, "is_anomaly"] = True
df.loc[mask, "anomaly_type"] = "traffic_spike"


# ============================================================
# 14. ANOMALY 2 — CONVERSION CRASH
# ============================================================

conversion_date = "2025-03-15"

mask = df["date"] == conversion_date

df.loc[mask, "conversion_rate"] = (
    df.loc[mask, "conversion_rate"] * 0.35
)

df.loc[mask, "orders"] = (
    df.loc[mask, "visitors"]
    * df.loc[mask, "conversion_rate"]
    / 100
).astype(int)

df.loc[mask, "revenue"] = (
    df.loc[mask, "orders"]
    * average_order_value[mask.to_numpy()]
)

df.loc[mask, "is_anomaly"] = True
df.loc[mask, "anomaly_type"] = "conversion_crash"


# ============================================================
# 15. ANOMALY 3 — REFUND SPIKE
# ============================================================

refund_date = "2025-05-20"

mask = df["date"] == refund_date

df.loc[mask, "refunds"] = (
    df.loc[mask, "refunds"] * 6
).astype(int)

df.loc[mask, "is_anomaly"] = True
df.loc[mask, "anomaly_type"] = "refund_spike"


# ============================================================
# 16. ANOMALY 4 — REVENUE COLLAPSE
# ============================================================

revenue_date = "2025-08-10"

mask = df["date"] == revenue_date

df.loc[mask, "revenue"] = (
    df.loc[mask, "revenue"] * 0.45
)

df.loc[mask, "is_anomaly"] = True
df.loc[mask, "anomaly_type"] = "revenue_collapse"


# ============================================================
# 17. ANOMALY 5 — CHECKOUT INCIDENT
# ============================================================

checkout_date = "2025-10-25"

mask = df["date"] == checkout_date

# Conversion drops
df.loc[mask, "conversion_rate"] = (
    df.loc[mask, "conversion_rate"] * 0.30
)

# Orders fall because conversion falls
df.loc[mask, "orders"] = (
    df.loc[mask, "visitors"]
    * df.loc[mask, "conversion_rate"]
    / 100
).astype(int)

# Revenue falls
df.loc[mask, "revenue"] = (
    df.loc[mask, "revenue"] * 0.35
)

# Refunds increase
df.loc[mask, "refunds"] = (
    df.loc[mask, "refunds"] * 5
).astype(int)

df.loc[mask, "is_anomaly"] = True
df.loc[mask, "anomaly_type"] = "checkout_incident"


# ============================================================
# 18. SAVE DATASET
# ============================================================

df.to_csv(
    "data/business_data.csv",
    index=False
)


# ============================================================
# 19. VERIFICATION
# ============================================================

print("Business dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Known anomalies: {df['is_anomaly'].sum()}")

print("\nAnomaly types:")
print(
    df[df["is_anomaly"]]["anomaly_type"].value_counts()
)