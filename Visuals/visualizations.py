"""
Visualization functions for anomaly analytics dashboard.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# CORRELATION HEATMAP


def correlation_heatmap(df):


    plt.figure(figsize=(10, 6))

    sns.heatmap(
        df.corr(numeric_only=True),
        annot=True,
        cmap="coolwarm"
    )

    plt.title("Correlation Heatmap")

    return plt



# ANOMALY DISTRIBUTION


def anomaly_distribution(df, column_name):


    fig = px.histogram(
        df,
        x=column_name,
        color=column_name,
        title="Anomaly Distribution"
    )

    return fig


# ANOMALY TREND OVER TIME


def anomaly_trend_chart(df):

    suspicious_df = df[
        df["Anomaly"] == "Suspicious"
    ]

    trend_data = (
        suspicious_df
        .groupby("date")
        .size()
        .reset_index(name="Suspicious_Count")
    )

    fig = px.line(
        trend_data,
        x="date",
        y="Suspicious_Count",
        title="Suspicious Enrollment Trend Over Time",
        markers=True
    )

    return fig



# PINCODE-WISE SUSPICIOUS COUNT

def pincode_anomaly_chart(df):


    suspicious_df = df[
        df["Anomaly"] == "Suspicious"
    ]

    pincode_data = (
        suspicious_df
        .groupby("pincode")
        .size()
        .reset_index(name="Suspicious_Count")
    )

    fig = px.bar(
        pincode_data,
        x="pincode",
        y="Suspicious_Count",
        title="Pincode-wise Suspicious Activity"
    )

    return fig