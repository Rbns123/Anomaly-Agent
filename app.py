import streamlit as st
import pandas as pd
import numpy as np


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Business Anomaly Agent",
    page_icon="🔎",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .main-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 17px;
            color: #9aa0a6;
            margin-bottom: 25px;
        }

        .anomaly-box {
            padding: 20px;
            border-radius: 12px;
            background-color: #2b1717;
            border-left: 6px solid #ff4b4b;
            margin-bottom: 20px;
        }

        .success-box {
            padding: 20px;
            border-radius: 12px;
            background-color: #172b1c;
            border-left: 6px solid #21c55d;
        }

        .root-box {
            padding: 20px;
            border-radius: 12px;
            background-color: #172235;
            border-left: 6px solid #4da3ff;
            margin-top: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🔎 AI Business Anomaly Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Detect anomalies, investigate root causes, analyze evidence, '
    'and generate business recommendations.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR - DATA INPUT
# ============================================================

st.sidebar.header("📂 Data Input")

uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)


# ============================================================
# LOAD DATA
# ============================================================

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.sidebar.success(
        f"Uploaded successfully: {len(df)} rows"
    )

else:

    default_path = "data/anomaly_results.csv"

    try:
        df = pd.read_csv(default_path)

        st.sidebar.info(
            "Using project sample dataset"
        )

    except FileNotFoundError:

        st.error(
            "No dataset found. Please upload a CSV file."
        )

        st.stop()

# ============================================================
# DATA VALIDATION & COLUMN UNDERSTANDING
# ============================================================

st.subheader("🧠 Data Understanding")

# Check whether the uploaded dataset has enough data
if len(df) < 10:
    st.warning(
        "⚠️ The dataset contains very few records. "
        "More data will produce more reliable anomaly detection."
    )

# Identify numeric columns
numeric_columns_preview = list(
    df.select_dtypes(include=np.number).columns
)

# Identify possible date columns
possible_date_columns = []

for column in df.columns:

    column_name = column.lower()

    if any(
        word in column_name
        for word in ["date", "time", "timestamp"]
    ):
        possible_date_columns.append(column)


# Display validation status

if len(numeric_columns_preview) >= 2:

    st.success(
        f"✅ Dataset is suitable for anomaly analysis. "
        f"Found {len(numeric_columns_preview)} numeric metrics."
    )

else:

    st.error(
        "❌ Dataset is not suitable for anomaly analysis. "
        "At least 2 numeric business metrics are required."
    )


# Display detected columns

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 📊 Numeric Metrics")

    if numeric_columns_preview:

        for column in numeric_columns_preview:

            st.write(f"✅ {column}")

    else:

        st.write("No numeric metrics detected.")


with col2:

    st.markdown("### 📅 Date / Time Columns")

    if possible_date_columns:

        for column in possible_date_columns:

            st.write(f"📅 {column}")

    else:

        st.write(
            "No obvious date column detected."
        )        


# ============================================================
# BASIC DATA CLEANING
# ============================================================

df = df.copy()

# Remove completely empty rows
df = df.dropna(how="all")

# Reset index
df = df.reset_index(drop=True)


# ============================================================
# DATASET OVERVIEW
# ============================================================

st.subheader("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Rows",
        len(df)
    )

with col2:
    st.metric(
        "Columns",
        len(df.columns)
    )

with col3:
    numeric_count = len(
        df.select_dtypes(include=np.number).columns
    )

    st.metric(
        "Numeric Columns",
        numeric_count
    )

with col4:
    missing_values = int(df.isnull().sum().sum())

    st.metric(
        "Missing Values",
        missing_values
    )


# ============================================================
# DATE COLUMN
# ============================================================

st.subheader("⚙️ Configure Analysis")

all_columns = list(df.columns)

date_options = ["None"] + all_columns

date_column = st.selectbox(
    "Select Date Column",
    date_options
)

if date_column != "None":

    try:
        df[date_column] = pd.to_datetime(
            df[date_column]
        )

        df = df.sort_values(
            date_column
        ).reset_index(drop=True)

    except Exception:

        st.warning(
            "The selected date column could not be converted to a date."
        )


# ============================================================
# NUMERIC COLUMNS
# ============================================================

numeric_columns = list(
    df.select_dtypes(include=np.number).columns
)

if len(numeric_columns) < 2:

    st.error(
        "Your dataset needs at least two numeric columns "
        "for anomaly detection."
    )

    st.stop()


# ============================================================
# METRIC SELECTION
# ============================================================

selected_metrics = st.multiselect(
    "Select business metrics to analyze",
    numeric_columns,
    default=numeric_columns[:min(6, len(numeric_columns))]
)


if len(selected_metrics) == 0:

    st.warning(
        "Please select at least one metric."
    )

    st.stop()


# ============================================================
# DISPLAY RAW DATA
# ============================================================

with st.expander("👀 View Uploaded Data"):

    st.dataframe(
        df,
        use_container_width=True
    )


# ============================================================
# ANOMALY DETECTION
# ============================================================

st.subheader("🚨 Anomaly Detection")

st.write(
    "The agent uses statistical Z-score analysis to identify "
    "unusual business behavior."
)


# Make sure selected metrics are numeric
analysis_df = df[selected_metrics].apply(
    pd.to_numeric,
    errors="coerce"
)


# Calculate Z-scores
mean_values = analysis_df.mean()
std_values = analysis_df.std().replace(0, np.nan)

z_scores = (
    analysis_df - mean_values
) / std_values

# ============================================================
# SMART ANOMALY DETECTION
# ============================================================

absolute_z = z_scores.abs()

# Count how many metrics are significantly abnormal
df["anomaly_metric_count"] = (
    absolute_z >= 3
).sum(axis=1)

# Maximum abnormality across all selected metrics
df["max_zscore"] = absolute_z.max(axis=1)

# Detect an anomaly when:
# 1. At least two business metrics are strongly abnormal
# OR
# 2. One metric is extremely abnormal
df["is_anomaly"] = (
    (df["anomaly_metric_count"] >= 2)
    | (df["max_zscore"] >= 4)
)


# ============================================================
# ANOMALY SUMMARY
# ============================================================

anomaly_count = int(
    df["is_anomaly"].sum()
)

normal_count = len(df) - anomaly_count


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Records",
        len(df)
    )

with col2:

    st.metric(
        "Detected Anomalies",
        anomaly_count
    )

with col3:

    st.metric(
        "Normal Records",
        normal_count
    )


# ============================================================
# ANOMALY CHART
# ============================================================

st.subheader("📈 Business Metrics")

chart_columns = selected_metrics

chart_data = df[chart_columns].copy()

st.line_chart(
    chart_data,
    use_container_width=True
)


# ============================================================
# ANOMALY TABLE
# ============================================================

if anomaly_count > 0:

    st.subheader("🔴 Detected Anomalies")

    anomaly_table = df[
        df["is_anomaly"] == True
    ].copy()

    display_columns = []

    if date_column != "None":
        display_columns.append(date_column)

    display_columns += selected_metrics

    display_columns.append("max_zscore")

    st.dataframe(
        anomaly_table[display_columns],
        use_container_width=True
    )

else:

    st.success(
        "No significant anomalies were detected."
    )

    st.stop()


# ============================================================
# SELECT ANOMALY
# ============================================================

st.subheader("🔬 Investigate an Anomaly")

anomaly_indices = list(
    anomaly_table.index
)

selected_index = st.selectbox(
    "Select an anomaly to investigate",
    anomaly_indices,
    format_func=lambda x: (
        str(df.loc[x, date_column])
        if date_column != "None"
        else f"Record {x}"
    )
)


selected_row = df.loc[
    selected_index
]


# ============================================================
# CREATE BASELINE
# ============================================================

normal_data = df[
    df["is_anomaly"] == False
]

if len(normal_data) == 0:

    st.warning(
        "There are not enough normal records to create "
        "a baseline."
    )

    st.stop()


baseline = normal_data[
    selected_metrics
].mean()


# ============================================================
# CALCULATE PERCENTAGE CHANGES
# ============================================================

changes = {}

for metric in selected_metrics:

    normal_value = baseline[metric]

    anomaly_value = selected_row[metric]

    if normal_value != 0:

        change = (
            (anomaly_value - normal_value)
            / abs(normal_value)
        ) * 100

    else:

        change = 0

    changes[metric] = change


# ============================================================
# EVIDENCE
# ============================================================

st.subheader("📌 Evidence")

evidence_df = pd.DataFrame(
    {
        "Metric": selected_metrics,
        "Normal Baseline": [
            baseline[m]
            for m in selected_metrics
        ],
        "Anomaly Value": [
            selected_row[m]
            for m in selected_metrics
        ],
        "Change from Baseline (%)": [
            changes[m]
            for m in selected_metrics
        ]
    }
)

st.dataframe(
    evidence_df,
    use_container_width=True
)


# ============================================================
# ROOT CAUSE ENGINE
# ============================================================

def find_metric(
    keywords,
    available_metrics
):

    for metric in available_metrics:

        metric_lower = metric.lower()

        for keyword in keywords:

            if keyword in metric_lower:

                return metric

    return None


visitors_metric = find_metric(
    ["visitor", "traffic", "sessions", "users"],
    selected_metrics
)

conversion_metric = find_metric(
    ["conversion"],
    selected_metrics
)

orders_metric = find_metric(
    ["order", "purchase", "transaction"],
    selected_metrics
)

revenue_metric = find_metric(
    ["revenue", "sales"],
    selected_metrics
)

refund_metric = find_metric(
    ["refund", "return"],
    selected_metrics
)

marketing_metric = find_metric(
    ["marketing", "advertising", "ad_spend"],
    selected_metrics
)


# ============================================================
# ROOT CAUSE CLASSIFICATION
# ============================================================

root_cause = "general_business_anomaly"

confidence = "MEDIUM"

explanation = (
    "Multiple business metrics deviated significantly "
    "from their normal baseline."
)


# CHECKOUT / PAYMENT
if (
    conversion_metric
    and orders_metric
    and refund_metric
):

    if (
        changes[conversion_metric] < -30
        and changes[orders_metric] < -30
        and changes[refund_metric] > 100
    ):

        root_cause = "checkout_problem"

        confidence = "VERY HIGH"

        explanation = (
            "Conversion and orders collapsed while "
            "refunds increased sharply, suggesting "
            "a checkout or payment failure."
        )


# CONVERSION
elif (
    conversion_metric
    and visitors_metric
):

    if (
        changes[conversion_metric] < -30
        and changes[visitors_metric] > -20
    ):

        root_cause = "conversion_problem"

        confidence = "HIGH"

        explanation = (
            "Traffic remained relatively stable, "
            "but the conversion rate dropped significantly."
        )


# REFUNDS
elif refund_metric:

    if changes[refund_metric] > 100:

        root_cause = "refund_problem"

        confidence = "HIGH"

        explanation = (
            "Refunds increased significantly compared "
            "with the normal business baseline."
        )


# REVENUE
elif revenue_metric:

    if changes[revenue_metric] < -30:

        root_cause = "revenue_problem"

        confidence = "HIGH"

        explanation = (
            "Revenue decreased significantly compared "
            "with the normal business baseline."
        )


# MARKETING
elif (
    marketing_metric
    and revenue_metric
):

    if (
        changes[marketing_metric] > 40
        and changes[revenue_metric] < 0
    ):

        root_cause = "marketing_problem"

        confidence = "MEDIUM"

        explanation = (
            "Marketing spending increased while "
            "revenue decreased."
        )


# ============================================================
# ROOT CAUSE DISPLAY
# ============================================================

st.subheader("🧠 Root Cause Analysis")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        f"""
        <div class="root-box">

        <h3>Likely Root Cause</h3>

        <h2>{root_cause.upper()}</h2>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="root-box">

        <h3>Confidence</h3>

        <h2>{confidence}</h2>

        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    f"""
    <div class="root-box">

    <h3>Analytical Explanation</h3>

    <p>{explanation}</p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BUSINESS IMPACT
# ============================================================

st.subheader("💼 Business Impact")

if revenue_metric:

    revenue_change = changes[
        revenue_metric
    ]

    if revenue_change < 0:

        st.error(
            f"Revenue decreased by "
            f"{abs(revenue_change):.2f}% "
            f"from the normal baseline."
        )

    else:

        st.info(
            f"Revenue increased by "
            f"{revenue_change:.2f}% "
            f"from the normal baseline."
        )


# ============================================================
# RECOMMENDATIONS
# ============================================================

st.subheader("💡 Recommended Actions")


recommendations = []


if root_cause == "checkout_problem":

    recommendations = [
        "Immediately check checkout and payment gateway logs.",
        "Test the complete purchase journey using multiple payment methods.",
        "Check whether the payment provider reported an outage.",
        "Review failed transactions and error codes."
    ]


elif root_cause == "conversion_problem":

    recommendations = [
        "Review the landing page and purchase funnel.",
        "Check for recent website or UI changes.",
        "Analyze device and browser-level conversion rates.",
        "Compare conversion performance across traffic sources."
    ]


elif root_cause == "refund_problem":

    recommendations = [
        "Investigate the main reasons for refunds.",
        "Check recent product or service quality issues.",
        "Review customer complaints.",
        "Analyze refund patterns by product and customer segment."
    ]


elif root_cause == "revenue_problem":

    recommendations = [
        "Check order volume and average order value.",
        "Investigate pricing or product changes.",
        "Compare revenue across major customer segments.",
        "Review recent marketing and sales performance."
    ]


elif root_cause == "marketing_problem":

    recommendations = [
        "Review recent advertising campaigns.",
        "Compare marketing spend with conversion performance.",
        "Pause poorly performing campaigns.",
        "Analyze return on advertising spend."
    ]


else:

    recommendations = [
        "Investigate the metrics showing the largest deviation.",
        "Compare the anomaly against recent business events.",
        "Check operational and technical logs.",
        "Analyze the affected customer or product segments."
    ]


for i, recommendation in enumerate(
    recommendations,
    start=1
):

    st.write(
        f"**{i}.** {recommendation}"
    )


# ============================================================
# ANOMALY DETAIL
# ============================================================

st.subheader("📋 Selected Anomaly Details")

detail_data = {
    "Metric": selected_metrics,
    "Change from Baseline": [
        f"{changes[m]:.2f}%"
        for m in selected_metrics
    ],
    "Z-Score": [
        f"{z_scores.loc[selected_index, m]:.2f}"
        for m in selected_metrics
    ]
}

detail_df = pd.DataFrame(
    detail_data
)

st.dataframe(
    detail_df,
    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "AI Business Anomaly Agent • "
    "Local statistical anomaly detection + "
    "root cause reasoning"
)