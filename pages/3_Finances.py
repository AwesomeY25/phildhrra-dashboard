import streamlit as st
import pandas as pd
import altair as alt

# Set page title and icon
st.set_page_config(page_title="Finance Dashboard", page_icon="💰")

# Define file paths and sheet names
file_path = 'resources/This Year - Consolidator Sheet.xlsx'
sources_sheet = "Sources"
mobilization_sheet = "Resource Mobilization"

def finance_dashboard(sources_df: pd.DataFrame, mobilization_df: pd.DataFrame) -> None:
    # Grants Data per Year (Line Graph)
    st.write("### Grants Over the Years")
    if "Year" in sources_df.columns and "Grant" in sources_df.columns:
        grant_data = sources_df[['Year', 'Grant']].dropna()
        if not grant_data.empty:
            line_chart = alt.Chart(grant_data).mark_line(point=True).encode(
                x=alt.X('Year:O', title="Year"),
                y=alt.Y('Grant:Q', title="Grant Amount"),
                tooltip=['Year', 'Grant']
            ).properties(title="Grants Over the Years")
            st.altair_chart(line_chart, use_container_width=True)
        else:
            st.write("No grant data available.")

    # Financial Breakdown by Source (Bar Chart)
    st.write("### Financial Breakdown by Source")
    revenue_sources = sources_df.drop(columns=["Year", "Organization"], errors='ignore')
    revenue_data = revenue_sources.melt(var_name="Source", value_name="Amount").dropna()
    if not revenue_data.empty:
        bar_chart = alt.Chart(revenue_data).mark_bar().encode(
            x=alt.X('Source:N', sort='-y', title="Source"),
            y=alt.Y('Amount:Q', title="Total Amount"),
            tooltip=['Source', 'Amount']
        ).properties(title="Financial Breakdown by Source")
        st.altair_chart(bar_chart, use_container_width=True)
    else:
        st.write("No financial data available.")

    # Donor Names Pie Chart
    st.write("### Donor Funding Distribution")
    if "Donor/Funder" in mobilization_df.columns and "Amount" in mobilization_df.columns:
        mobilization_df["Amount"] = pd.to_numeric(mobilization_df["Amount"], errors='coerce')
        donor_data = mobilization_df.groupby('Donor/Funder')["Amount"].sum().reset_index()
        if not donor_data.empty:
            pie_chart = alt.Chart(donor_data).mark_arc().encode(
                theta=alt.Theta(field="Amount", type="quantitative"),
                color=alt.Color(field="Donor/Funder", type="nominal"),
                tooltip=["Donor/Funder", "Amount"]
            ).properties(title="Funding Distribution by Donor")
            st.altair_chart(pie_chart, use_container_width=True)
        else:
            st.write("No donor data available.")
    
    # Organization Finances Table
    st.write("### Finances per Organization")
    if "Organization" in sources_df.columns:
        organizations = sources_df["Organization"].dropna().unique()
        selected_org = st.selectbox('Select Organization', organizations)
        filtered_data = sources_df[sources_df["Organization"] == selected_org]
        if not filtered_data.empty:
            st.write(f"Finance data for {selected_org}:")
            st.table(filtered_data)
        else:
            st.write(f"No data available for {selected_org}.")

try:
    # Load both sheets
    sources_df = pd.read_excel(file_path, sheet_name=sources_sheet)
    mobilization_df = pd.read_excel(file_path, sheet_name=mobilization_sheet)

    st.markdown("# Finance Dashboard")
    
    if sources_df.empty or mobilization_df.empty:
        st.info("One of the sheets is empty. Please check the data.")
    else:
        finance_dashboard(sources_df, mobilization_df)

except Exception as e:
    st.error(f"Failed to load data from the Excel file. Error: {e}")