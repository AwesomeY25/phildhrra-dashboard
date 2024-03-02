from typing import Any
import streamlit as st
import pandas as pd
import os

def animation_demo(df: pd.DataFrame) -> None:
    # Display the DataFrame as a table
    st.write(df)

st.set_page_config(page_title="Projects", page_icon="📹")
st.markdown("# Projects")

# Path to your CSV file
file_path = r'.\resources\DestinationSheet.csv'
# Read the CSV file into a Pandas DataFrame, skipping the first row and using the second row as headers
df = pd.read_csv(file_path, skiprows=1, header=0)

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
