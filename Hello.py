# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import pandas as pd

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Log In",
        page_icon="👋",
    )

    st.write("# Welcome to PhilDHRRA! 👋")

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

if __name__ == "__main__":
    run()