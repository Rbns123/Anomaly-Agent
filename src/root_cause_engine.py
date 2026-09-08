# ============================================================
# GENERIC ROOT CAUSE ENGINE
# Works with different CSV datasets
# ============================================================

import pandas as pd
import numpy as np


def find_root_cause(
    df,
    anomaly_row,
    numeric_columns,
    anomaly_index=None
):
    """
    Generic root-cause analysis.

    Works with any dataset containing numeric columns.
    Does not assume business-specific columns such as
    revenue, refunds, or conversion_rate.
    """

    # --------------------------------------------------------
    # 1. SAFETY CHECKS
    # --------------------------------------------------------

    if df is None or df.empty:
        return {
            "root_cause": "INSUFFICIENT_DATA",
            "confidence": "LOW",
            "explanation": "The dataset is empty.",
            "evidence": [],
            "recommendations": [
                "Upload a dataset containing usable records."
            ]
        }

    if not numeric_columns:
        return {
            "root_cause": "NO_NUMERIC_METRICS",
            "confidence": "LOW",
            "explanation": (
                "No numeric columns were available for "
                "anomaly analysis."
            ),
            "evidence": [],
            "recommendations": [
                "Select at least two numeric columns."
            ]
        }

    # --------------------------------------------------------
    # 2. CLEAN NUMERIC COLUMNS
    # --------------------------------------------------------

    valid_columns = []

    for column in numeric_columns:

        if column not in df.columns:
            continue

        converted = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        if converted.notna().sum() > 0:
            valid_columns.append(column)

    if not valid_columns:
        return {
            "root_cause": "NO_VALID_METRICS",
            "confidence": "LOW",
            "explanation": (
                "The selected numeric columns do not "
                "contain usable numeric values."
            ),
            "evidence": [],
            "recommendations": [
                "Choose columns containing numeric measurements."
            ]
        }

    # --------------------------------------------------------
    # 3. CREATE NORMAL BASELINE
    # --------------------------------------------------------

    baseline = {}

    for column in valid_columns:

        values = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()

        if len(values) > 0:
            baseline[column] = values.median()

    # --------------------------------------------------------
    # 4. CALCULATE DEVIATION
    # --------------------------------------------------------

    evidence = []

    for column in valid_columns:

        if column not in baseline:
            continue

        normal_value = baseline[column]

        try:
            anomaly_value = pd.to_numeric(
                pd.Series([anomaly_row[column]]),
                errors="coerce"
            ).iloc[0]
        except Exception:
            continue

        # Ignore missing anomaly values
        if pd.isna(anomaly_value):
            continue

        # Avoid division by zero
        if normal_value == 0:

            if anomaly_value == 0:
                percentage_change = 0
            else:
                percentage_change = np.nan

        else:

            percentage_change = (
                (anomaly_value - normal_value)
                / abs(normal_value)
            ) * 100

        if pd.isna(percentage_change):
            continue

        evidence.append({
            "metric": column,
            "normal_value": float(normal_value),
            "anomaly_value": float(anomaly_value),
            "change_percent": float(percentage_change),
            "absolute_change": abs(float(percentage_change))
        })

    # --------------------------------------------------------
    # 5. SORT BY MOST IMPORTANT DEVIATION
    # --------------------------------------------------------

    evidence.sort(
        key=lambda x: x["absolute_change"],
        reverse=True
    )

    # Keep strongest evidence
    strongest_evidence = evidence[:5]

    # --------------------------------------------------------
    # 6. DETERMINE ROOT CAUSE
    # --------------------------------------------------------

    if not strongest_evidence:

        root_cause = "GENERAL_DATA_ANOMALY"
        confidence = "LOW"

        explanation = (
            "The selected record was detected as unusual, "
            "but there was not enough valid numeric evidence "
            "to identify a specific cause."
        )

    else:

        largest = strongest_evidence[0]

        largest_metric = largest["metric"]
        largest_change = largest["change_percent"]

        number_of_large_changes = sum(
            1
            for item in strongest_evidence
            if item["absolute_change"] >= 30
        )

        # Strong anomaly
        if abs(largest_change) >= 100:

            root_cause = (
                f"SIGNIFICANT_DEVIATION_IN_{largest_metric.upper()}"
            )

            confidence = "HIGH"

        elif abs(largest_change) >= 50:

            root_cause = (
                f"MAJOR_DEVIATION_IN_{largest_metric.upper()}"
            )

            confidence = "HIGH"

        elif abs(largest_change) >= 25:

            root_cause = (
                f"DEVIATION_IN_{largest_metric.upper()}"
            )

            confidence = "MEDIUM"

        else:

            root_cause = "GENERAL_DATA_ANOMALY"
            confidence = "MEDIUM"

        # Build explanation
        direction = (
            "increased"
            if largest_change > 0
            else "decreased"
        )

        explanation = (
            f"The strongest deviation was observed in "
            f"'{largest_metric}', which {direction} by "
            f"{abs(largest_change):.2f}% compared with the "
            f"normal baseline."
        )

        if number_of_large_changes > 1:

            explanation += (
                f" {number_of_large_changes} metrics showed "
                f"large deviations, suggesting that the anomaly "
                f"is associated with a broader change in the "
                f"dataset rather than a single value."
            )

    # --------------------------------------------------------
    # 7. GENERATE RECOMMENDATIONS
    # --------------------------------------------------------

    recommendations = []

    if strongest_evidence:

        main_metric = strongest_evidence[0]["metric"]

        recommendations.append(
            f"Investigate the '{main_metric}' metric first."
        )

        recommendations.append(
            "Compare the anomalous record with nearby "
            "normal records."
        )

        recommendations.append(
            "Check whether the same pattern appears "
            "in other records."
        )

        recommendations.append(
            "Review the source system or process that "
            "generated the affected metric."
        )

        recommendations.append(
            "Check for missing, incorrect, or unusual "
            "input values."
        )

    else:

        recommendations.append(
            "Review the selected anomaly manually."
        )

        recommendations.append(
            "Check the dataset for missing or invalid values."
        )

    # --------------------------------------------------------
    # 8. RETURN RESULT
    # --------------------------------------------------------

    return {
        "root_cause": root_cause,
        "confidence": confidence,
        "explanation": explanation,
        "evidence": strongest_evidence,
        "recommendations": recommendations
    }


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("GENERIC ROOT CAUSE ENGINE")
    print("=" * 60)

    test_data = pd.DataFrame({
        "customers": [100, 105, 98, 110, 102],
        "sales": [5000, 5200, 5100, 5050, 12000],
        "returns": [5, 4, 6, 5, 7]
    })

    test_anomaly = test_data.iloc[4]

    result = find_root_cause(
        df=test_data,
        anomaly_row=test_anomaly,
        numeric_columns=[
            "customers",
            "sales",
            "returns"
        ]
    )

    print("\nROOT CAUSE:")
    print(result["root_cause"])

    print("\nCONFIDENCE:")
    print(result["confidence"])

    print("\nEXPLANATION:")
    print(result["explanation"])

    print("\nEVIDENCE:")

    for item in result["evidence"]:
        print(
            f"- {item['metric']}: "
            f"{item['change_percent']:.2f}%"
        )

    print("\nRECOMMENDATIONS:")

    for number, recommendation in enumerate(
        result["recommendations"],
        start=1
    ):
        print(f"{number}. {recommendation}")

    print("\n" + "=" * 60)
    print("ROOT CAUSE ENGINE TEST COMPLETE")
    print("=" * 60)