from typing import Any
import streamlit as st
import pandas as pd
import altair as alt

# Set page title and icon
st.set_page_config(page_title="Finance Dashboard", page_icon="💰")

def finance_dashboard(df: pd.DataFrame) -> None:
    # Display a high-level overview
    st.write("### Average of Sources of Income or Revenues")
    sources_df = df[['Source', 'Amount in PHP - Past Year', 'Amount in PHP - Current Year']].copy()
    st.table(sources_df)

    # Grants Data per Year (Line Graph)
    st.write("### Grants Over the Years")
    grant_data = df[df['Source'] == 'Grant'][['Year', 'Amount']].dropna()
    if not grant_data.empty:
        line_chart = alt.Chart(grant_data).mark_line(point=True).encode(
            x=alt.X('Year:O', title="Year"),
            y=alt.Y('Amount:Q', title="Grant Amount"),
            tooltip=['Year', 'Amount']
        ).properties(title="Grants Over the Years")
        st.altair_chart(line_chart, use_container_width=True)
    else:
        st.write("No grant data available.")

    # Top Organizations with Grants (Bar Chart)
    st.write("### Top Organizations with Grants")
    org_grants = df[df['Source'] == 'Grant'].groupby('Organization')['Amount'].sum().reset_index()
    if not org_grants.empty:
        org_grants = org_grants.sort_values(by='Amount', ascending=False).head(10)
        bar_chart = alt.Chart(org_grants).mark_bar().encode(
            x=alt.X('Organization:O', sort='-y', title="Organization"),
            y=alt.Y('Amount:Q', title="Total Grant Amount"),
            tooltip=['Organization', 'Amount']
        ).properties(title="Top 10 Organizations with Grants")
        st.altair_chart(bar_chart, use_container_width=True)
    else:
        st.write("No organization grant data available.")

    # Donor Names Pie Chart
    st.write("### Donor Names Distribution")
    donor_data = df[['Donor/Funder', 'Amount']].dropna()
    if not donor_data.empty:
        donor_distribution = donor_data.groupby('Donor/Funder')['Amount'].sum().reset_index()
        donor_distribution.columns = ['Donor', 'Total Amount']

        pie_chart = alt.Chart(donor_distribution).mark_arc().encode(
            theta=alt.Theta(field="Total Amount", type="quantitative"),
            color=alt.Color(field="Donor", type="nominal"),
            tooltip=["Donor", "Total Amount"]
        ).properties(title="Funding Distribution by Donor")
        st.altair_chart(pie_chart, use_container_width=True)
    else:
        st.write("No donor data available.")

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