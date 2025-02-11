import streamlit as st
from database import authenticate_user
from reset_password import show_reset_password 
from streamlit_extras.switch_page_button import switch_page



def show():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.error("Please enter both email and password")
        elif authenticate_user(email, password):
         st.success("Login successful!")
         switch_page('home') 
        else:
            st.error("Invalid email or password. Please sign up if you don’t have an account.")

    if st.button("Forgot Password?"):
        st.session_state.page = "Reset Password"
        st.rerun()
        

if __name__ == "__main__":
    show()
    


