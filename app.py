import streamlit as st
from login import show as show_login
from signup import show as show_signup
from home import show_home_page  # Assuming your home page logic is in home.py or add to your main file

# Set up session state for user login (check if username is present)
if "username" not in st.session_state:
    st.session_state.username = None

# Streamlit interface (Navigation Bar)
st.set_page_config(page_title="Library Booking System", layout="wide")

# Navigation across the top
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("Home"):
        if st.session_state.username:
            show_home_page()  # Show home page if logged in
        else:
            st.warning("Please log in first.")
with col2:
    if st.button("Log In"):
        show_login()  # Direct to login page
with col3:
    if st.button("Sign Up"):
        show_signup()  # Direct to sign-up page
with col4:
    if st.button("Logout"):
        st.session_state.username = None
        st.success("Logged out successfully.")
        st.experimental_rerun()

# # Main logic
# if st.session_state.username:  # If the user is logged in
#     show_home_page()  # Show home page if logged in
# else:
#     show_landing()  # If not logged in, show landing page with login/sign-up options
