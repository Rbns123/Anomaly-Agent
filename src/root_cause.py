import pandas as pd


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("data/anomaly_results.csv")


# ============================================================
# 2. BUSINESS FEATURES
# ============================================================

features = [
    "visitors",
    "conversion_rate",
    "orders",
    "revenue",
    "refunds",
    "marketing_spend"
]


# ============================================================
# 3. FIND Z-SCORE ANOMALIES
# ============================================================

anomalies = df[
    df["zscore_anomaly"] == True
].copy()


# ============================================================
# 4. CREATE NORMAL BASELINE
# ============================================================

normal_data = df[
    df["zscore_anomaly"] == False
]


baseline = normal_data[
    features
].mean()


# ============================================================
# 5. ROOT CAUSE CLASSIFICATION FUNCTION
# ============================================================

def classify_root_cause(changes):

    visitors = changes["visitors"]
    conversion = changes["conversion_rate"]
    orders = changes["orders"]
    revenue = changes["revenue"]
    refunds = changes["refunds"]
    marketing = changes["marketing_spend"]


    # CHECKOUT / PAYMENT PROBLEM
    if (
        conversion < -30
        and orders < -30
        and refunds > 100
    ):
        return (
            "checkout_problem",
            "VERY HIGH",
            "Conversion and orders collapsed while "
            "refunds increased sharply, suggesting a "
            "checkout or payment failure."
        )


    # CONVERSION PROBLEM
    if (
        conversion < -30
        and visitors > -20
    ):
        return (
            "conversion_problem",
            "HIGH",
            "Traffic was relatively stable, but "
            "conversion rate dropped significantly."
        )


    # REFUND PROBLEM
    if refunds > 100:
        return (
            "refund_problem",
            "HIGH",
            "Refunds increased significantly compared "
            "with the normal baseline."
        )


    # REVENUE PROBLEM
    if revenue < -30:
        return (
            "revenue_problem",
            "HIGH",
            "Revenue decreased significantly compared "
            "with the normal baseline."
        )


    # MARKETING PROBLEM
    if marketing > 40 and revenue < 0:
        return (
            "marketing_problem",
            "MEDIUM",
            "Marketing spending increased while "
            "revenue decreased."
        )


    # GENERAL
    return (
        "general_business_anomaly",
        "MEDIUM",
        "Multiple business metrics deviated "
        "from their normal baseline."
    )


    # --------------------------------------------------------
    # TRAFFIC PROBLEM
    # --------------------------------------------------------

    if visitors > 40:

        return (
            "traffic_problem",
            "HIGH",
            "Traffic increased significantly."
        )


    # --------------------------------------------------------
    # CONVERSION PROBLEM
    # --------------------------------------------------------

    if (
        conversion < -30
        and visitors > -20
    ):

        return (
            "conversion_problem",
            "HIGH",
            "Traffic was relatively stable, "
            "but conversion rate dropped significantly."
        )


    # --------------------------------------------------------
    # CHECKOUT / PAYMENT PROBLEM
    # --------------------------------------------------------

    if (
        conversion < -30
        and orders < -30
        and refunds > 100
    ):

        return (
            "checkout_problem",
            "VERY HIGH",
            "Conversion and orders collapsed while "
            "refunds increased sharply, suggesting a "
            "checkout or payment failure."
        )


    # --------------------------------------------------------
    # REFUND PROBLEM
    # --------------------------------------------------------

    if refunds > 100:

        return (
            "refund_problem",
            "HIGH",
            "Refunds increased significantly compared "
            "with the normal baseline."
        )


    # --------------------------------------------------------
    # REVENUE PROBLEM
    # --------------------------------------------------------

    if revenue < -30:

        return (
            "revenue_problem",
            "HIGH",
            "Revenue decreased significantly compared "
            "with the normal baseline."
        )


    # --------------------------------------------------------
    # MARKETING PROBLEM
    # --------------------------------------------------------

    if marketing > 40 and revenue < 0:

        return (
            "marketing_problem",
            "MEDIUM",
            "Marketing spending increased while "
            "revenue decreased."
        )


    # --------------------------------------------------------
    # GENERAL BUSINESS ANOMALY
    # --------------------------------------------------------

    return (
        "general_business_anomaly",
        "MEDIUM",
        "Multiple business metrics deviated "
        "from their normal baseline."
    )


# ============================================================
# 6. ANALYZE EACH ANOMALY
# ============================================================

print("\n==========================================")
print("       AI ROOT CAUSE ANALYSIS")
print("==========================================\n")


for index, row in anomalies.iterrows():

    print("\n")
    print("=" * 60)

    print(
        f"DATE: {row['date']}"
    )

    print(
        f"KNOWN TYPE: {row['anomaly_type']}"
    )

    print("=" * 60)


    # --------------------------------------------------------
    # Calculate percentage changes
    # --------------------------------------------------------

    changes = {}


    for feature in features:

        normal_value = baseline[feature]

        anomaly_value = row[feature]


        if normal_value != 0:

            percentage_change = (
                (anomaly_value - normal_value)
                / normal_value
            ) * 100

        else:

            percentage_change = 0


        changes[feature] = percentage_change


    # --------------------------------------------------------
    # Classify root cause
    # --------------------------------------------------------

    root_cause, confidence, explanation = (
        classify_root_cause(changes)
    )


    # --------------------------------------------------------
    # Display root cause
    # --------------------------------------------------------

    print(
        f"\n🚨 ROOT CAUSE: "
        f"{root_cause.upper()}"
    )

    print(
        f"CONFIDENCE: {confidence}"
    )


    print(
        f"\nEXPLANATION:"
    )

    print(
        explanation
    )


    # --------------------------------------------------------
    # Display evidence
    # --------------------------------------------------------

    print(
        "\nEVIDENCE:"
    )


    for feature in features:

        print(
            f"  {feature:<20}"
            f"{changes[feature]:>8.2f}%"
        )


print("\n")
print("=" * 60)
print("       ROOT CAUSE ANALYSIS COMPLETE")
print("=" * 60)