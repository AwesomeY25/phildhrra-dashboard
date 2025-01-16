from typing import Any
import streamlit as st
import pandas as pd
from pathlib import Path
import pickle
import streamlit_authenticator as stauth

st.set_page_config(page_title="Projects", page_icon="📹")

def animation_demo(df: pd.DataFrame) -> None:
    # Display the DataFrame as a table
    st.write(df)

# Load data from the Excel file
excel_file_path = 'resources/This Year - Consolidator Sheet.xlsx'  # Use forward slashes or double backslashes
sheet_name = 'Programs and Activities'

try:
    # Read the Excel file
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    
    st.markdown("# Programs and Activities")

    # Select options for organization and program type
    organizations = df['Organization'].unique()
    organizations = ['All'] + list(organizations)
    selected_ngo = st.selectbox('Select Organization: ', organizations)

    program_types = df['Program Type'].unique()
    program_types = ['All'] + list(program_types)
    selected_program_type = st.selectbox('Select Program Type: ', program_types)
     
    # Filter DataFrame based on selected options
    if selected_ngo == 'All' and selected_program_type == 'All':
        filtered_df = df
    elif selected_ngo == 'All':
        filtered_df = df[df['Program Type'] == selected_program_type]
    elif selected_program_type == 'All':
        filtered_df = df[df['Organization'] == selected_ngo]
    else:
        filtered_df = df[(df['Organization'] == selected_ngo) & (df['Program Type'] == selected_program_type)]

    # Display the filtered DataFrame
    animation_demo(filtered_df)

except Exception as e:
    st.error(f"Failed to load data from {sheet_name}. Error: {e}")