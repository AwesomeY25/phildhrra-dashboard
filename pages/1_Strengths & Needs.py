import streamlit as st
import pandas as pd

# Load the Excel file
file_path = 'resources\This Year - Consolidator Sheet.xlsx'
xls = pd.ExcelFile(file_path)

# Define sheet names
sheets_to_display = {
    "Basic Profile": ["Name of NGO", "Address (Main):", "Telephone/Telefax:", "E-mail Address:", "Website:", "Facebook Link:", "Instagram Link:", "Twitter Link:", "Name of Exclusive Director:", "Mobile No. of ED", "Name of Admin/Finance/Office Manager:"],
    "Organizational Strengths": ["Organization", "Strengths/Expertise", "Rating"],
    "Capacity Development Programs": ["Organization", "Title of Training", "Estimated Date", "Location (Region, City)", "Training Organizer/Provider"],
    "Capacity DevelopmentTraining Ne": ["Organization", "Capacity Needs of the Organization", "Reason/s"]
}

# Streamlit app
st.title("NGO Strengths and Weaknesses")

# Loop through the specified sheets
for sheet, columns in sheets_to_display.items():
    st.header(sheet)

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
    else:
        # Add filtering based on Organization if the column exists
        if "Organization" in df.columns:
            unique_organizations = df["Organization"].dropna().unique()
            selected_org = st.selectbox(f"Filter by Organization in {sheet}", unique_organizations, key=sheet)

            # Filter the data based on the selected organization
            filtered_data = df[df["Organization"] == selected_org]
            st.subheader(f"Trainings for{selected_org}")
            st.dataframe(filtered_data)
        else:
            st.dataframe(df)

        # Create basic visualizations if numerical data exists
        if any(df.dtypes == 'float64') or any(df.dtypes == 'int64'):
            st.subheader("Visualizations")
            numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

            for column in numeric_columns:
                st.bar_chart(df[column])