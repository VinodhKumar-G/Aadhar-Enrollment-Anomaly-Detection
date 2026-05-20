import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df= pd.read_csv(r"C:\Users\pranj\Aadhar-Enrollment-Anomaly-Detection\Data\aadhar_enrollment_bengaluru_rural.csv")

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])
df = df.sort_values('date')

df['total_enrollment'] = (
    df['age_0_5'] +
    df['age_5_17'] +
    df['age_18_greater']
)



monthly_enrollment= df.groupby('date')['total_enrollment'].sum().reset_index()
fig= px.line(
    monthly_enrollment,
    x='date',
    y= 'total_enrollment'
)

pincode= df.groupby('pincode')['total_enrollment'].sum().reset_index()

fig2= px.bar(
    pincode,
    x='pincode',
    y= 'total_enrollment'
)
fig2.update_traces(width=2)

age_monthly = df.groupby('date')[['age_0_5','age_5_17','age_18_greater']].sum().reset_index()
fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x=age_monthly['date'],
    y=age_monthly['age_0_5'],
    mode='lines',
    name='Age 0–5'
))

fig3.add_trace(go.Scatter(
    x=age_monthly['date'],
    y=age_monthly['age_5_17'],
    mode='lines',
    name='Age 5–17'
))

fig3.add_trace(go.Scatter(
    x=age_monthly['date'],
    y=age_monthly['age_18_greater'],
    mode='lines',
    name='Age 18+'
))

fig3.update_layout(
    xaxis_title='Date',
    yaxis_title='Enrollments',
    width=1000,
    height=500,
    legend_title='Age Groups'
)

fig3.update_xaxes(tickangle=45)

st.header("Dashboard")
st.subheader("Monthly distribution of AadharEnrollments")

st.plotly_chart(fig,use_container_width=True)

st.subheader("Area wise distribution of Aadhar Enrollments")
st.plotly_chart(fig2,use_container_width=True)

st.subheader("Age wise Monthly distribution of Aadhar Enrollments")
st.plotly_chart(fig3,use_container_width=True)