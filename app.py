import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Financial Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Financial Intelligence Dashboard")

file_path = "Phase 1.xlsx"

# Load Data
raw_df = pd.read_excel(file_path, sheet_name="Raw Data")

raw_df["Date"] = pd.to_datetime(raw_df["Date"])

# KPIs
revenue = raw_df[raw_df["Type"] == "Revenue"]["Amount"].sum()
expenses = raw_df[raw_df["Type"] == "Expense"]["Amount"].sum()
profit = revenue - expenses

monthly_expense = (
    raw_df[raw_df["Type"] == "Expense"]
    .groupby(raw_df["Date"].dt.to_period("M"))["Amount"]
    .sum()
    .mean()
)

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"₹{revenue:,.0f}")
col2.metric("Expenses", f"₹{expenses:,.0f}")
col3.metric("Profit", f"₹{profit:,.0f}")
col4.metric("Burn Rate", f"₹{monthly_expense:,.0f}")

st.divider()

# Revenue Trend
st.subheader("📈 Revenue Trend")

revenue_df = (
    raw_df[raw_df["Type"] == "Revenue"]
    .groupby(raw_df["Date"].dt.strftime("%Y-%m"))["Amount"]
    .sum()
    .reset_index()
)

revenue_df.columns = ["Month", "Revenue"]

fig1 = px.line(
    revenue_df,
    x="Month",
    y="Revenue",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# Expense Breakdown
st.subheader("💰 Expense Breakdown")

expense_df = (
    raw_df[raw_df["Type"] == "Expense"]
    .groupby("Category")["Amount"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    expense_df,
    names="Category",
    values="Amount"
)

st.plotly_chart(fig2, use_container_width=True)

# Vendor Analysis
st.subheader("🏢 Top Vendors")

vendor_df = (
    raw_df.groupby("Vendor")["Amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .head(10)
)

fig3 = px.bar(
    vendor_df,
    x="Vendor",
    y="Amount"
)

st.plotly_chart(fig3, use_container_width=True)

# Transaction Data
st.subheader("📋 Transaction Details")

st.dataframe(raw_df, use_container_width=True)
