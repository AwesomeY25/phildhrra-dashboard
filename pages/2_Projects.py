from typing import Any
import streamlit as st
import pandas as pd
from io import StringIO

def animation_demo(df: pd.DataFrame) -> None:
    # Display the DataFrame as a table
    st.write(df)

st.set_page_config(page_title="Projects", page_icon="📹")
st.markdown("# Projects")


csv_data = """
Organization,Program Type,Programs/Projects Services,No. of Beneficiaries,Area Coverage (Pls. Specify Name of Areas),Area Coverage (Pls. Specify Name of Areas),Area Coverage (Pls. Specify Name of Areas)
NGO 1,Sustainable Agricultural Productivity/Natural Resource Management,Sample Project,1200,Laguna,Something,Something
NGO 2,Sustainable Agricultural Productivity/Natural Resource Management,Sample Project,1200,Pampanga,Something na,Something na
NGO 2,Sustainable Agricultural Productivity/Natural Resource Management,Sample Project,1200,Laguna,Something pa,Something pa
NGO 1,Basic Social Services Delivery,Sample Project,1200,Laguna,Something,Something
NGO 1,Basic Social Services Delivery,Sample Project,1200,Pampanga,Something na,Something na
NGO 2,Basic Social Services Delivery,Sample Project,1200,Laguna,Something,Something
NGO 2,Basic Social Services Delivery,Sample Project,1200,Pampanga,Something na,Something na
"""

# Convert CSV data to DataFrame
df = pd.read_csv(StringIO(csv_data), skiprows=1, header=0)

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
