import streamlit as st
from database import authenticate_user

def show():
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.success("Login successful!")
            st.switch_page("landing.py")  # Redirect to the landing page
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    show()
