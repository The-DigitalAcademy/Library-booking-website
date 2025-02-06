import streamlit as st
from login import show as show_login
from signup import show as show_signup
from home import show as show_home
from reset_password import show_reset_password

st.set_page_config(page_title="Library Booking", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Login"

if st.session_state.page == "Login":
    show_login()
elif st.session_state.page == "Sign Up":
    show_signup()
elif st.session_state.page == "Home":
    show_home()
elif st.session_state.page == "Reset Password":
    show_reset_password()

