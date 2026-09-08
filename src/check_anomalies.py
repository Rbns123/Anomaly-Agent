import pandas as pd


# Load the dataset
df = pd.read_csv("data/business_data.csv")


# Select only known anomaly rows
anomalies = df[df["is_anomaly"] == True]


print("\n========== KNOWN ANOMALIES ==========\n")


print(
    anomalies[
        [
            "date",
            "visitors",
            "conversion_rate",
            "orders",
            "revenue",
            "refunds",
            "anomaly_type"
        ]
    ].to_string(index=False)
)


print("\n======================================")
print(f"Total known anomalies: {len(anomalies)}")
print("======================================")