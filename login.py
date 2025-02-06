import streamlit as st
from database import authenticate_user
from reset_password import show_reset_password 

def show():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Add login authentication logic here
        if email and password:
            st.success("Login successful!")
            st.session_state.page = "Home"
            st.rerun()

        else:
            st.error("Invalid credentials")

    if st.button("Forgot Password?"):
        st.session_state.page = "Reset Password"
        st.rerun()


