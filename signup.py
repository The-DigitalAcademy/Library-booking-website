import streamlit as st
from database import create_user

def show():
    st.title("Sign Up")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if create_user(username, email, password):
            st.success("Account created successfully! Please log in.")
        else:
            st.error("Username or email already exists!")

if __name__ == "__main__":
    show()
