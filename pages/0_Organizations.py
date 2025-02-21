import streamlit as st
import pandas as pd
import os

# Load the Excel file
file_path = 'resources/This Year - Consolidator Sheet.xlsx'
if not os.path.exists(file_path):
    st.error(f"File not found: {file_path}")

xls = pd.ExcelFile(file_path)

# Define sheet names and desired columns (ensure the names match exactly those in your Excel file)
sheets_to_display = {
    "Basic Profiles": [
        "Name of NGO:",
        "Address (Main):",
        "Telephone/Telefax:",
        "E-mail Address:",
        "Website:",
        "Facebook Link:",
        "Instagram Link:",
        "Twitter Link:",
        "Name of Exclusive Director:",
        "Mobile No. of ED",
        "Name of Admin/Finance/Office Manager:",
    ]
}

# Streamlit app title
st.title("Organization's Information")

# Loop through the specified sheets
for sheet, columns in sheets_to_display.items():
    st.header(sheet)

    # Check if the sheet exists in the file
    if sheet not in xls.sheet_names:
        st.warning(f"Sheet '{sheet}' not found in the file.")
        continue

    # Load the data and filter columns if specified
    df = xls.parse(sheet)
    if columns:
        available_cols = [col for col in columns if col in df.columns]
        df = df[available_cols]

    # Check if the sheet has data
    if df.empty:
        st.info(f"No data available in the '{sheet}' sheet.")
    else:
        # Process the Basic Profiles sheet
        if sheet == "Basic Profiles":
            # Check that the NGO name column exists and use it to list unique organizations
            if "Name of NGO:" in df.columns:
                unique_organizations = df["Name of NGO:"].dropna().unique()
            else:
                st.error("The column 'Name of NGO:' was not found in the data.")
                continue

            selected_ngo = st.selectbox("Select an NGO", unique_organizations)

            if selected_ngo:
                # Filter data for the selected NGO
                filtered_data = df[df["Name of NGO:"] == selected_ngo]
                ngo_data = filtered_data.iloc[0]

                # Build the basic profile dictionary with all desired fields
                user_profile = {
                    'Name': ngo_data.get("Name of NGO:", "N/A"),
                    'Address': ngo_data.get("Address (Main):", "N/A"),
                    'Telephone': ngo_data.get("Telephone/Telefax:", "N/A"),
                    'Email': ngo_data.get("E-mail Address:", "N/A"),
                    'Website': ngo_data.get("Website:", "N/A"),
                    'Facebook': ngo_data.get("Facebook Link:", "N/A"),
                    'Instagram': ngo_data.get("Instagram Link:", "N/A"),
                    'Twitter': ngo_data.get("Twitter Link:", "N/A"),
                    'Executive Director Name': ngo_data.get("Name of Exclusive Director:", "N/A"),
                    'Mobile of ED': ngo_data.get("Mobile No. of ED", "N/A"),
                    'Admin/Finance Manager Name': ngo_data.get("Name of Admin/Finance/Office Manager:", "N/A")
                }

                st.write(f"### Profile for {selected_ngo}")
                
                # Show the filtered data for detailed view
                st.subheader("Detailed Data")
                st.dataframe(filtered_data.T)  # Transpose the DataFrame before displaying

                # Now display data from other sheets based on the selected NGO
                for other_sheet in ["Advocacy", "Accreditations", "Awards", "Knowledge & Learning Management"]:
                    st.header(other_sheet)

                    # Load the data for the other sheets
                    other_df = xls.parse(other_sheet)

                    # Check if the other sheet has data
                    if other_df.empty:
                        st.info(f"No data available in the '{other_sheet}' sheet.")
                    else:
                        # Filter the data based on the selected NGO
                        if "Name of NGO:" in other_df.columns:
                            filtered_other_data = other_df[other_df["Name of NGO:"] == selected_ngo]
                        else:
                            filtered_other_data = other_df  # If no NGO column, show all data

                        if filtered_other_data.empty:
                            st.info(f"No data available for '{selected_ngo}' in the '{other_sheet}' sheet.")
                        else:
                            st.dataframe(filtered_other_data)