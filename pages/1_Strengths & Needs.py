import streamlit as st
import pandas as pd
import altair as alt

# Load the Excel file
file_path = 'resources/This Year - Consolidator Sheet.xlsx'
xls = pd.ExcelFile(file_path)

# Define sheet names
sheets_to_display = {
    "Capacity Development Programs": ["Organization", "Title of Training", "Estimated Date", "Location (Region, City)", "Training Organizer/Provider"],
    "Capacity DevelopmentTraining Ne": ["Organization", "Capacity Needs of the Organization", "Reason/s"]
}

# Streamlit app
st.title("NGO Strengths and Weaknesses Dashboard")

# Loop through the specified sheets
for sheet, columns in sheets_to_display.items():

    # Check if the sheet exists in the file
    if sheet not in xls.sheet_names:
        st.warning(f"Sheet '{sheet}' not found in the file.")
        continue

    # Load the data
    df = xls.parse(sheet)

    # Filter columns if specified
    if columns:
        df = df[[col for col in columns if col in df.columns]]

    # Check if the sheet has data
    if df.empty:
        st.info(f"No data available in the '{sheet}' sheet.")
        continue

    # Filtering system based on Organization
    if "Organization" in df.columns:
        unique_organizations = df["Organization"].dropna().unique()
        selected_org = st.selectbox(f"Filter by Organization", unique_organizations, key=f"org_{sheet}")

        # Filter the data based on the selected organization
        filtered_data = df[df["Organization"] == selected_org]
        st.subheader(f"Details for {selected_org}")
        st.dataframe(filtered_data)
    else:
        st.dataframe(df)

    # Filtering system based on Location or Area
    if "Location (Region, City)" in df.columns:
        unique_locations = df["Location (Region, City)"].dropna().unique()
        selected_location = st.selectbox(f"Filter by Location", unique_locations, key=f"loc_{sheet}")

        # Filter the data based on the selected location
        filtered_data = df[df["Location (Region, City)"] == selected_location]
        st.subheader(f"Details for {selected_location}")
        st.dataframe(filtered_data)

    # Visualizations for numerical data
    if any(df.dtypes == 'float64') or any(df.dtypes == 'int64'):
        st.subheader("Numerical Data Visualizations")
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

        for column in numeric_columns:
            st.write(f"**Bar Chart for {column}**")
            st.bar_chart(df[column])

    # Pie chart for categorical data
    if "Organization" in df.columns:
        st.subheader("Categorical Data Distribution")
        org_counts = df["Organization"].value_counts().reset_index()
        org_counts.columns = ["Organization", "Count"]

        pie_chart = alt.Chart(org_counts).mark_arc().encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Organization", type="nominal"),
            tooltip=["Organization", "Count"]
        ).properties(title="Organization Distribution")
        st.altair_chart(pie_chart, use_container_width=True)