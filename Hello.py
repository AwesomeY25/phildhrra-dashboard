import streamlit as st
from pathlib import Path
import pandas as pd

def run():
    st.set_page_config(page_title="Excel File Viewer", page_icon="📊")

    st.write("# Welcome to PhilDHRRA! 👋")
    st.write("### Upload and View an Excel File")

    # File upload feature
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])

    if uploaded_file:
        # Save the uploaded file
        resources_dir = Path("resources")
        resources_dir.mkdir(exist_ok=True)

        file_save_path = resources_dir / uploaded_file.name
        with open(file_save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File uploaded and saved as: {file_save_path}")

        # Read all sheets
        try:
            excel_data = pd.ExcelFile(file_save_path)
            sheet_names = excel_data.sheet_names  # Get all sheet names

            st.write("### Available Sheets:")
            for sheet in sheet_names:
                st.write(f"- {sheet}")

            # Loop through each sheet and display headers + first few rows
            for sheet in sheet_names:
                st.write(f"## 📄 Sheet: {sheet}")
                df = pd.read_excel(file_save_path, sheet_name=sheet)

                if not df.empty:
                    # Display headers
                    st.write("### Columns:", list(df.columns))

                    # Display first few rows
                    st.dataframe(df.head(10))  
                else:
                    st.warning(f"⚠️ The sheet '{sheet}' is empty.")

        except Exception as e:
            st.error(f"Error reading the file: {e}")

if __name__ == "__main__":
    run()