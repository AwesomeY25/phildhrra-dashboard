from typing import Any

import streamlit as st
import pandas as pd

import pickle
from pathlib import Path
import streamlit_authenticator as stauth

st.set_page_config(page_title="Organizations", page_icon="\ud83c\udfe2")

names = ["John Smith", "Jose Rizal"]
usernames = ["johnsmith", "jrizal"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "phildhrra_dashboard", "abcdef", cookie_expiry_days=0)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False: 
    st.error("Username/Password is Incorrect")

if authentication_status == None: 
    st.warning("Please enter your username and password")

if authentication_status: 

    def display_ngo_info(ngo_data: dict, ngo_name: str) -> None:
        st.write(f"### {ngo_name}")
        ngo_info_df = pd.DataFrame.from_dict(ngo_data[ngo_name], orient='index', columns=['Information'])
        st.table(ngo_info_df)

    authenticator.logout("Logout", "sidebar")
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
            'Strengths': ['Transparency', 'Community Engagement', 'Financial Stability']
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
            'Strengths': ['Efficiency', 'Innovation', 'Impactful Programs']
        }
    }

    # File upload feature
    st.write("**Upload an Excel File:**")
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])

    if uploaded_file:
        # Save the uploaded file to the resources directory
        resources_dir = Path("resources")
        resources_dir.mkdir(exist_ok=True)

        file_save_path = resources_dir / uploaded_file.name
        with open(file_save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File uploaded and saved as: {file_save_path}")

        # Display uploaded file content
        try:
            excel_data = pd.read_excel(file_save_path)
            st.write("**Uploaded File Content:**")
            st.dataframe(excel_data)
        except Exception as e:
            st.error(f"Error reading the file: {e}")

    # Create a DataFrame with the names of NGOs
    ngo_names_df = pd.DataFrame({'NGO Names': list(ngo_data.keys())})

    # Display the table of NGO names
    st.write("**All Members:**")
    st.table(ngo_names_df)

    st.write("**View Organization Details:**")
    # Selectbox to choose which NGO to display
    selected_ngo = st.selectbox('Select NGO', list(ngo_data.keys()))

    # Display the selected NGO information
    display_ngo_info(ngo_data, selected_ngo)