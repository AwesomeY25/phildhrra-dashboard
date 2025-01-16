from typing import Any
import streamlit as st
import pandas as pd

import pickle
from pathlib import Path

# Set page title and icon
st.set_page_config(page_title="Finance Dashboard", page_icon="💰")

def finance_dashboard(df: pd.DataFrame) -> None:
    # Display a high-level overview
    st.write("### Average of Sources of Income or Revenues")
        
    sources_df = df[['Source', 'Amount in PHP - Past Year', 'Amount in PHP - Current Year']].copy()
    st.table(sources_df)
        
    # Display Grants Data per Year
    st.write("### Grants Data per Year")
    grant_data = df[df['Source'] == 'Grant'][['Year', 'Amount']].dropna()
    if not grant_data.empty:
        st.line_chart(grant_data.set_index('Year'))  # Line chart for grants per year
    else:
        st.write("No grant data available.")
        
    # Finances per Organization
    st.write("### Finances per Organization")
    organizations = df['Organization'].unique()
    selected_ngo = st.selectbox('Select Organization', organizations)

    filtered_data = df[df['Organization'] == selected_ngo]
    if not filtered_data.empty:
        st.write(f"Finance data for {selected_ngo}:")
        st.table(filtered_data[['Source', 'Amount in PHP - Past Year', 'Amount in PHP - Current Year']])
    else:
        st.write(f"No data available for {selected_ngo}.")

    # Donor Organizations and Funding Partners
    st.write("## Donor Organizations and Funding Partners")
    st.write("If major sources of funds are grants, indicate funding partner or donor organization and grant amount for the past 3 years.")
    donor_data = df[['Donor/Funder', 'Project Funded', 'Year(s) Covered', 'Amount']].dropna()
    st.table(donor_data)
        
# Load data from the Excel file
excel_file_path = 'resources/This Year - Consolidator Sheet.xlsx'
sheet_name = 'Resource Mobilization'

try:
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    st.markdown("# Finance Dashboard")

    # Check if the sheet has data
    if df.empty:
        st.info(f"No data available in the '{sheet_name}' sheet.")
    else:
        # Call the finance dashboard function if data is loaded
        finance_dashboard(df)

except Exception as e:
    st.error(f"Failed to load data from {sheet_name}. Error: {e}")