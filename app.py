import streamlit as st
from login import show as show_login
from signup import show as show_signup

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Login", "Sign Up"])

if page == "Login":
    show_login()
else:
    show_signup()
