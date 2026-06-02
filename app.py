import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Financial Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Financial Intelligence Dashboard")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file:

    raw_df = pd.read_excel(uploaded_file, sheet_name="Raw Data")

    uploaded_file.seek(0)
    expense_df = pd.read_excel(uploaded_file, sheet_name="Expense Tracker")

    uploaded_file.seek(0)
    metrics_df = pd.read_excel(uploaded_file, sheet_name="Initial Metrics")

    raw_df["Date"] = pd.to_datetime(raw_df["Date"])

    revenue = raw_df.loc[
        raw_df["Type"] == "Revenue",
        "Amount"
    ].sum()

    expenses = raw_df.loc[
        raw_df["Type"] == "Expense",
        "Amount"
    ].sum()

    profit = revenue - expenses

    monthly_expense = (
        raw_df[raw_df["Type"] == "Expense"]
        .groupby(raw_df["Date"].dt.to_period("M"))
        ["Amount"]
        .sum()
        .mean()
    )

    st.markdown("## Financial Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Revenue",
        f"₹{revenue:,.0f}"
    )

    c2.metric(
        "Expenses",
        f"₹{expenses:,.0f}"
    )

    c3.metric(
        "Profit",
        f"₹{profit:,.0f}"
    )

    c4.metric(
        "Burn Rate",
        f"₹{monthly_expense:,.0f}"
    )

    st.divider()

    raw_df["Month"] = raw_df["Date"].dt.strftime("%Y-%m")

    monthly_revenue = (
        raw_df[raw_df["Type"] == "Revenue"]
        .groupby("Month")["Amount"]
        .sum()
        .reset_index()
    )

    revenue_chart = px.line(
        monthly_revenue,
        x="Month",
        y="Amount",
        title="Revenue Trend"
    )

    st.plotly_chart(
        revenue_chart,
        use_container_width=True
    )

    expense_breakdown = (
        raw_df[raw_df["Type"] == "Expense"]
        .groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )

    pie_chart = px.pie(
        expense_breakdown,
        names="Category",
        values="Amount",
        title="Expense Breakdown"
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

    cashflow = (
        raw_df.groupby(
            [raw_df["Date"].dt.strftime("%Y-%m"), "Type"]
        )["Amount"]
        .sum()
        .unstack(fill_value=0)
        .reset_index()
    )

    cashflow["Net Cash Flow"] = (
        cashflow["Revenue"]
        - cashflow["Expense"]
    )

    cash_chart = px.bar(
        cashflow,
        x="Date",
        y="Net Cash Flow",
        title="Monthly Cash Flow"
    )

    st.plotly_chart(
        cash_chart,
        use_container_width=True
    )

    st.subheader("Top Vendors")

    vendor_table = (
        raw_df.groupby("Vendor")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .head(10)
    )

    st.dataframe(
        vendor_table,
        use_container_width=True
    )

    st.subheader("Business Metrics")

    metric_values = metrics_df.iloc[2:]

    st.dataframe(
        metric_values,
        use_container_width=True
    )
