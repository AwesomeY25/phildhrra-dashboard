import pickle
from pathlib import Path

import streamlit_authenticator as stauth
# from streamlit_authenticator.utilities.hasher import Hasher - if using latest streamlit version

names = ["John Smith", "Jose Rizal"]
usernames = ["johnsmith", "jrizal"]
passwords = ["abc123", "def456"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)

