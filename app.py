import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Financial Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Financial Intelligence Dashboard")

# Read Excel file from GitHub repository
file_path = "Phase 1.xlsx"

# Load workbook
xls = pd.ExcelFile(file_path)

# Show available sheets
st.subheader("Available Sheets")
st.write(xls.sheet_names)

# Preview each sheet
for sheet in xls.sheet_names:
    st.subheader(f"📄 {sheet}")
    df = pd.read_excel(file_path, sheet_name=sheet)
    st.dataframe(df.head())
