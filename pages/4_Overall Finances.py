from typing import Any
import streamlit as st
import pandas as pd

def finance_dashboard() -> None:
    
    st.write("### Average of Sources of Income or Revenues")
    sources_data = {
        'Source': ['Grant', 'Dues', 'Service Fees (Consultancy)', 'Donations',
                   'Gains from Investments (interest earnings)', 'Endowment fund',
                   'Social Enterprises', 'Others (Specify)'],
        'Amount in PHP - Past Year': ['', '', '', '', '', '', '', ''],
        'Amount in PHP - Current Year': ['', '', '', '', '', '', '', '']
    }
    sources_df = pd.DataFrame(sources_data)
    st.table(sources_df)
    
    st.write("### Grants Data per Year")
    grant_data = {
        'Year': [2019, 2020, 2021],
        'Grant Amount': [50000, 34000, 70000]  # Example data, replace with actual grant amounts
    }
    grant_df = pd.DataFrame(grant_data)
    st.line_chart(grant_df.set_index('Year'))  # Line chart for grants per year

    st.write("## Donor Organizations and Funding Partners")

    # Display information about major sources of funds and grants
    st.write("If major sources of funds are grants, indicate funding partner or donor organization and grant amount for the past 3 years.")
    grant_data = {
        'Donor/Funder': ['', '', ''],
        'Amount': ['', '', '']
    }
    grant_df = pd.DataFrame(grant_data)
    st.table(grant_df)
    
# Set page title and icon
st.set_page_config(page_title="Overall Finance Dashboard", page_icon="💰")
# Display the title
st.markdown("# Overall Finance Dashboard")
# Display the finance dashboard
finance_dashboard()
