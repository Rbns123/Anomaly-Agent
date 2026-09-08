import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("data/business_data.csv")


# ============================================================
# 2. SELECT FEATURES
# ============================================================

features = [
    "visitors",
    "conversion_rate",
    "orders",
    "revenue",
    "refunds",
    "marketing_spend"
]

X = df[features]


# ============================================================
# 3. STANDARDIZE FEATURES
# ============================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

X_scaled = pd.DataFrame(
    X_scaled,
    columns=features
)


# ============================================================
# 4. Z-SCORE DETECTION
# ============================================================

absolute_z_scores = X_scaled.abs()

df["max_z_score"] = absolute_z_scores.max(axis=1)

Z_THRESHOLD = 3.0

df["zscore_anomaly"] = (
    df["max_z_score"] > Z_THRESHOLD
)


zscore_anomalies = df[
    df["zscore_anomaly"] == True
]


print("\n==========================================")
print("          Z-SCORE DETECTION")
print("==========================================\n")

print(
    "Z-score threshold:",
    Z_THRESHOLD
)

print(
    "Total Z-score anomalies:",
    len(zscore_anomalies)
)


# ============================================================
# 5. ISOLATION FOREST
# ============================================================

model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42
)


# Train model
model.fit(X_scaled)


# Predict
predictions = model.predict(X_scaled)


# 1 = normal
# -1 = anomaly

df["isolation_forest_prediction"] = predictions

df["isolation_forest_anomaly"] = (
    predictions == -1
)


# ============================================================
# 6. ISOLATION FOREST SCORE
# ============================================================

df["isolation_forest_score"] = (
    model.decision_function(X_scaled)
)


isolation_anomalies = df[
    df["isolation_forest_anomaly"] == True
]


# ============================================================
# 7. DISPLAY ISOLATION FOREST RESULTS
# ============================================================

print("\n==========================================")
print("        ISOLATION FOREST DETECTION")
print("==========================================\n")

print(
    "Total Isolation Forest anomalies:",
    len(isolation_anomalies)
)


print("\n========== DETECTED ANOMALIES ==========\n")


print(
    isolation_anomalies[
        [
            "date",
            "isolation_forest_score",
            "visitors",
            "conversion_rate",
            "orders",
            "revenue",
            "refunds",
            "anomaly_type"
        ]
    ]
    .sort_values(
        "isolation_forest_score"
    )
    .to_string(index=False)
)


# ============================================================
# 8. EVALUATION
# ============================================================

# Actual ground truth
y_true = df["is_anomaly"].astype(int)


# Z-score predictions
y_pred_zscore = (
    df["zscore_anomaly"]
    .astype(int)
)


# Isolation Forest predictions
y_pred_isolation = (
    df["isolation_forest_anomaly"]
    .astype(int)
)


# ============================================================
# Z-SCORE METRICS
# ============================================================

z_precision = precision_score(
    y_true,
    y_pred_zscore,
    zero_division=0
)

z_recall = recall_score(
    y_true,
    y_pred_zscore,
    zero_division=0
)

z_f1 = f1_score(
    y_true,
    y_pred_zscore,
    zero_division=0
)


z_cm = confusion_matrix(
    y_true,
    y_pred_zscore
)


# ============================================================
# ISOLATION FOREST METRICS
# ============================================================

if_precision = precision_score(
    y_true,
    y_pred_isolation,
    zero_division=0
)

if_recall = recall_score(
    y_true,
    y_pred_isolation,
    zero_division=0
)

if_f1 = f1_score(
    y_true,
    y_pred_isolation,
    zero_division=0
)


if_cm = confusion_matrix(
    y_true,
    y_pred_isolation
)


# ============================================================
# DISPLAY EVALUATION
# ============================================================

print("\n==========================================")
print("              MODEL EVALUATION")
print("==========================================\n")


print("Z-SCORE")
print("------------------------------------------")

print(
    f"Precision : {z_precision:.4f}"
)

print(
    f"Recall    : {z_recall:.4f}"
)

print(
    f"F1 Score  : {z_f1:.4f}"
)

print("\nConfusion Matrix:")

print(z_cm)


print("\n\nISOLATION FOREST")
print("------------------------------------------")

print(
    f"Precision : {if_precision:.4f}"
)

print(
    f"Recall    : {if_recall:.4f}"
)

print(
    f"F1 Score  : {if_f1:.4f}"
)

print("\nConfusion Matrix:")

print(if_cm)


# ============================================================
# FINAL COMPARISON
# ============================================================

print("\n==========================================")
print("           MODEL COMPARISON")
print("==========================================\n")


print(
    f"{'Metric':<15}"
    f"{'Z-Score':<15}"
    f"{'Isolation Forest':<20}"
)

print("-" * 50)


print(
    f"{'Precision':<15}"
    f"{z_precision:<15.4f}"
    f"{if_precision:<20.4f}"
)

print(
    f"{'Recall':<15}"
    f"{z_recall:<15.4f}"
    f"{if_recall:<20.4f}"
)

print(
    f"{'F1 Score':<15}"
    f"{z_f1:<15.4f}"
    f"{if_f1:<20.4f}"
)
# ============================================================
# 9. SAVE RESULTS
# ============================================================

df.to_csv(
    "data/anomaly_results.csv",
    index=False
)


print(
    "\nResults saved to:"
)


print(
    "data/anomaly_results.csv"
)