# import streamlit as st
# from database import get_db_connection
# from pages.login import show as show_login
# from pages.signup import show as show_signup
# # from home import show as show_home
# from reset_password import  show_reset_password
# # from LandingPage import show as show_Landing_Page


# st.set_page_config(page_title="Library Booking", layout="wide")

# if "page" not in st.session_state:
#     st.session_state.page = "Login"

# # if st.session_state.page == "LandingPage":
# #     show_Landing_Page()
# if st.session_state.page == "Login":
#     show_login()
# elif st.session_state.page == "Sign Up":
#     show_signup()
# # elif st.session_state.page == "Home":
# #     show_home()
# elif st.session_state.page == "Reset Password":
#     show_reset_password()

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Malawi Library", layout="wide")

st.title("Welcome to Malawi Library")

st.write("This is a book reservation system where you can browse, add, and book books.")

# Navigation buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Log In"):
        switch_page('login')

with col2:
    if st.button("Sign Up"):
        switch_page('signup')


