import streamlit as st
import pandas as pd

# Load the Excel file
file_path = 'resources/This Year - Consolidator Sheet.xlsx'
xls = pd.ExcelFile(file_path)

# Define sheet names
sheets_to_display = {
    "Basic Profile": ["Name of NGO", "Address (Main):", "Telephone/Telefax:", "E-mail Address:", "Website:", "Facebook Link:", "Instagram Link:", "Twitter Link:", "Name of Exclusive Director:", "Mobile No. of ED", "Name of Admin/Finance/Office Manager:"],
}

# Streamlit app
st.title("Organization's Information")

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
        # Display the data
        st.subheader("Data Table")
        st.dataframe(df)

        # Display user profile info for Basic Profile sheet
        if sheet == "Basic Profile":
            unique_organizations = df["Name of NGO"].dropna().unique()
            selected_ngo = st.selectbox("Select an NGO", unique_organizations)

            if selected_ngo:
                filtered_data = df[df["Name of NGO"] == selected_ngo]
                ngo_data = filtered_data.iloc[0]
                user_profile = {
                    'Name': ngo_data.get("Name of NGO", "N/A"),
                    'Address': ngo_data.get("Address (Main):", "N/A"),
                    'Telephone': ngo_data.get("Telephone/Telefax:", "N/A"),
                    'Email': ngo_data.get("E-mail Address:", "N/A"),
                    'Website': ngo_data.get("Website:", "N/A"),
                    'Facebook': ngo_data.get("Facebook Link:", "N/A"),
                    'Instagram': ngo_data.get("Instagram Link:", "N/A"),
                    'Twitter': ngo_data.get("Twitter Link:", "N/A"),
                    'Executive Director Name': ngo_data.get("Name of Exclusive Director:", "N/A"),
                    'Mobile of ED': ngo_data.get("Mobile No. of ED", "N/A"),
                    'Admin/Finance Manager Name': ngo_data.get("Name of Admin/Finance/Office Manager:", "N/A"),
                }

                st.write(f"### Profile for {selected_ngo}")
                st.write(user_profile)

                # Display filtered data table
                st.subheader("Filtered Data Table")
                st.dataframe(filtered_data)

        # Create basic visualizations if numerical data exists
        if any(df.dtypes == 'float64') or any(df.dtypes == 'int64'):
            st.subheader("Visualizations")
            numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

            for column in numeric_columns:
                st.bar_chart(df[column])