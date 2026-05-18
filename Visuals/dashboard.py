"""
Interactive dashboard for Aadhaar Enrollment
Anomaly Detection analytics.
"""

import streamlit as st
import pandas as pd

from sklearn.ensemble import IsolationForest

from utils import load_data

from visualizations import (
    correlation_heatmap,
    anomaly_distribution,
    anomaly_trend_chart,
    pincode_anomaly_chart
)

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Aadhaar Anomaly Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# DASHBOARD TITLE
# ---------------------------------------------------

st.title("Aadhaar Enrollment Anomaly Dashboard")

st.markdown("""
Interactive analytics dashboard for visualizing
suspicious Aadhaar enrollment patterns.
""")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = load_data("../Data/aadhar_enrollment_bengaluru_rural.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(
    df["date"],
    dayfirst=True
)

# ---------------------------------------------------
# ANOMALY DETECTION
# ---------------------------------------------------

# Numerical columns used for anomaly detection
numerical_cols = [
    "age_0_5",
    "age_5_17",
    "age_18_greater"
]

# Feature matrix
X = df[numerical_cols]

# Isolation Forest model
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

# Predict anomalies
df["Anomaly"] = model.fit_predict(X)

# Convert labels to readable form
df["Anomaly"] = df["Anomaly"].map({
    1: "Normal",
    -1: "Suspicious"
})

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("Filter Anomaly Data")

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    [
        df["date"].min(),
        df["date"].max()
    ]
)

# Pincode filter
selected_pincode = st.sidebar.selectbox(
    "Select Pincode",
    ["All"] + sorted(
        df["pincode"].astype(str).unique().tolist()
    )
)

# ---------------------------------------------------
# FILTER DATAFRAME
# ---------------------------------------------------

filtered_df = df.copy()

# Apply date filter
if len(date_range) == 2:

    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["date"] >= pd.to_datetime(start_date)) &
        (filtered_df["date"] <= pd.to_datetime(end_date))
    ]

# Apply pincode filter
if selected_pincode != "All":

    filtered_df = filtered_df[
        filtered_df["pincode"].astype(str) == selected_pincode
    ]

# ---------------------------------------------------
# DASHBOARD METRICS
# ---------------------------------------------------

total_records = len(filtered_df)

suspicious_records = len(
    filtered_df[
        filtered_df["Anomaly"] == "Suspicious"
    ]
)

normal_records = len(
    filtered_df[
        filtered_df["Anomaly"] == "Normal"
    ]
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Records",
    total_records
)

col2.metric(
    "Suspicious Records",
    suspicious_records
)

col3.metric(
    "Normal Records",
    normal_records
)

# ---------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------

st.subheader("Dataset Preview")

st.dataframe(filtered_df.head())

# ---------------------------------------------------
# CORRELATION HEATMAP
# ---------------------------------------------------

st.subheader("Correlation Heatmap")

heatmap = correlation_heatmap(filtered_df)

st.pyplot(heatmap)

# ---------------------------------------------------
# ANOMALY DISTRIBUTION
# ---------------------------------------------------

st.subheader("Anomaly Distribution")

fig = anomaly_distribution(
    filtered_df,
    "Anomaly"
)

st.plotly_chart(fig)

# ---------------------------------------------------
# SUSPICIOUS ENROLLMENT TREND
# ---------------------------------------------------

st.subheader("Suspicious Enrollment Trend")

trend_fig = anomaly_trend_chart(filtered_df)

st.plotly_chart(trend_fig)

# ---------------------------------------------------
# PINCODE-WISE SUSPICIOUS ACTIVITY
# ---------------------------------------------------

st.subheader("Pincode-wise Suspicious Activity")

pincode_fig = pincode_anomaly_chart(filtered_df)

st.plotly_chart(pincode_fig)

# ---------------------------------------------------
# SUSPICIOUS RECORDS TABLE
# ---------------------------------------------------

st.subheader("Suspicious Enrollment Records")

suspicious_df = filtered_df[
    filtered_df["Anomaly"] == "Suspicious"
]

st.dataframe(suspicious_df)