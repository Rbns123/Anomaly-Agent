import pandas as pd
import plotly.express as px


# Load the business dataset
df = pd.read_csv("data/business_data.csv")


# -----------------------------
# Revenue chart
# -----------------------------

revenue_fig = px.line(
    data_frame=df,
    x="date",
    y="revenue",
    title="Daily Revenue"
)

revenue_fig.show()


# -----------------------------
# Visitors chart
# -----------------------------

visitor_fig = px.line(
    data_frame=df,
    x="date",
    y="visitors",
    title="Daily Website Visitors"
)

visitor_fig.show()


# -----------------------------
# Orders chart
# -----------------------------

orders_fig = px.line(
    data_frame=df,
    x="date",
    y="orders",
    title="Daily Orders"
)

orders_fig.show()


# -----------------------------
# Refunds chart
# -----------------------------

refunds_fig = px.line(
    data_frame=df,
    x="date",
    y="refunds",
    title="Daily Refunds"
)

refunds_fig.show()