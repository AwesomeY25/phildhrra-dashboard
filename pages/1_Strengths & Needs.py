from typing import Any

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Organizations", page_icon="🏢")
st.markdown("# Organizational Profile")

# Define NGO data
ngo_data = {
    'NGO 1': {
        'Name': 'Example NGO 1',
        'Address': '123 NGO Street, Cityville',
        'Telephone/Telefax': '+1234567890',
        'E-mail Address': 'info@examplengo1.org',
        'Website': 'www.examplengo1.org',
        'Facebook Link': 'www.facebook.com/examplengo1',
        'Social Media Links': 'twitter.com/examplengo1, instagram.com/examplengo1',
        'Name of Exclusive Director': 'John Doe',
        'Mobile No. of ED': '+1987654321',
        'Name of Admin/Finance/Office Manager': 'Jane Smith',
        'Mobile No.': '+1234567890',
        'Strengths': ['Transparency', 'Community Engagement', 'Financial Stability'],
        'Needs': ['Funding', 'Volunteers'],
        'Reasons': ['To expand programs', 'To reach more communities']
    },
    'NGO 2': {
        'Name': 'Sample NGO 2',
        'Address': '456 NGO Avenue, Townsville',
        'Telephone/Telefax': '+0987654321',
        'E-mail Address': 'info@samplengo2.org',
        'Website': 'www.samplengo2.org',
        'Facebook Link': 'www.facebook.com/samplengo2',
        'Social Media Links': 'twitter.com/samplengo2, instagram.com/samplengo2',
        'Name of Exclusive Director': 'Alice Johnson',
        'Mobile No. of ED': '+9876543210',
        'Name of Admin/Finance/Office Manager': 'Bob Brown',
        'Mobile No.': '+0987654321',
        'Strengths': ['Efficiency', 'Innovation', 'Impactful Programs'],
        'Needs': ['Training', 'Equipment'],
        'Reasons': ['To enhance skills', 'To improve service delivery']
    }
}

# Convert NGO data into a DataFrame
ngo_df = pd.DataFrame.from_dict(ngo_data, orient='index')

# Display the table for strengths
st.write("### NGO Strengths")
strengths_df = ngo_df['Strengths'].apply(lambda x: ', '.join(x))
st.table(strengths_df)

# Selectbox to choose which strength to filter by
selected_strength = st.selectbox('Select Strength', ['Transparency', 'Community Engagement', 'Financial Stability',
                                                     'Efficiency', 'Innovation', 'Impactful Programs'])

# Filter NGOs based on the selected strength
filtered_ngos = [ngo_name for ngo_name, ngo_info in ngo_data.items() if selected_strength in ngo_info['Strengths']]

# Display the selected NGOs with the selected strength
if filtered_ngos:
    st.write("**NGOs with Selected Strength:**")
    for name in filtered_ngos:
        st.write(f"- {name}")
else:
    st.write("No NGOs found with this strength.")

# Display the table for needs
st.write("### NGO Needs")
needs_df = ngo_df['Needs'].apply(lambda x: ', '.join(x))
st.table(needs_df)

# Selectbox to choose which need to filter by
selected_need = st.selectbox('Select Need', ['Funding', 'Volunteers', 'Training', 'Equipment'])

# Filter NGOs based on the selected need
filtered_ngos = [ngo_name for ngo_name, ngo_info in ngo_data.items() if selected_need in ngo_info['Needs']]

# Display the selected NGOs with the selected need
if filtered_ngos:
    st.write("**NGOs with Selected Need:**")
    for name in filtered_ngos:
        st.write(f"- {name}")
else:
    st.write("No NGOs found with this need.")
