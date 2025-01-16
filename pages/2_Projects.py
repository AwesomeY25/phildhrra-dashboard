from typing import Any
import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(page_title="Projects", page_icon="📹")

def animation_demo(df: pd.DataFrame) -> None:
    """Display the DataFrame and visualizations."""
    st.write("### Filtered Programs and Activities")
    st.dataframe(df)

    # Visualize Program Types (Pie Chart)
    if "Program Type" in df.columns:
        st.write("### Program Type Distribution")
        program_type_counts = df["Program Type"].value_counts().reset_index()
        program_type_counts.columns = ["Program Type", "Count"]
        
        pie_chart = alt.Chart(program_type_counts).mark_arc().encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Program Type", type="nominal"),
            tooltip=["Program Type", "Count"]
        ).properties(title="Program Type Distribution")
        st.altair_chart(pie_chart, use_container_width=True)

    # Visualize Organizations (Bar Chart)
    if "Organization" in df.columns:
        st.write("### Organization Participation")
        org_counts = df["Organization"].value_counts().reset_index()
        org_counts.columns = ["Organization", "Count"]

        bar_chart = alt.Chart(org_counts).mark_bar().encode(
            x=alt.X("Organization", sort="-y"),
            y="Count",
            color="Organization",
            tooltip=["Organization", "Count"]
        ).properties(title="Organization Involvement")
        st.altair_chart(bar_chart, use_container_width=True)

    # Demographics per Activity (Bar Chart)
    if "Demographics" in df.columns:
        st.write("### Demographics per Activity")
        demo_counts = df["Demographics"].value_counts().reset_index()
        demo_counts.columns = ["Demographics", "Count"]

        demo_chart = alt.Chart(demo_counts).mark_bar().encode(
            x=alt.X("Demographics", sort="-y"),
            y="Count",
            color="Demographics",
            tooltip=["Demographics", "Count"]
        ).properties(title="Demographics Distribution")
        st.altair_chart(demo_chart, use_container_width=True)

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

    # Display the filtered DataFrame and visualizations
    animation_demo(filtered_df)

except Exception as e:
    st.error(f"Failed to load data from {sheet_name}. Error: {e}")