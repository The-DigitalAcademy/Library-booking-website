  
import streamlit as st
from database import authenticate_user
from reset_password import show_reset_password 
from streamlit_extras.switch_page_button import switch_page


st.markdown("""
    <style>
        body {
           background-color: #FAF3E0;
            color: #333;
            font-family: 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .stApp {
            background-color: #FAF3E0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        
        .page-container {
            background-color: #ffffff;
            # padding: 30px;
            # border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            width: 350px;
            text-align: center;
            # margin: auto;
        }
        
        .stTextInput, .stButton {
            margin: 10px 0;
            padding: 10px;
            # border-radius: 12px;
            # border: 1px solid #333;
        }
        
        .stTextInput input {
            background-color: #444;
            color: #fff;
        }
        
        .stButton button {
           background-color: #2c3e50;
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            cursor: pointer;
            text-align: center;
            transition: 0.3s;
            font-weight: bold;
        }

        .stButton button:hover {
            background-color: #34495e;
        }
        
        .stError {
            background-color: #ff6b6b;
            color: #fff;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }

        .stSuccess {
            background-color: #28a745;
            color: #fff;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }

        h1 {
            font-size: 36px;
            margin-top: 50px;
        }
        
        .forgot-password {
            color: #007BFF;
            font-size: 14px;
            margin-top: 10px;
        }
        
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-container">', unsafe_allow_html=True)
st.subheader("📖 Malawi Booking Books System!")
def show():
    
    st.title("Log in")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.error("Please enter both email and password")
        else:
            user_id = authenticate_user(email, password)
            if user_id:
                st.session_state.user_id = user_id
                st.success("Login successful!")
                switch_page('home')
            else:
                st.error("Invalid email or password. Please sign up if you don’t have an account.")

    if st.button("Forgot Password?"):
        st.session_state.page = "Reset Password"
        st.rerun()       
st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show()
   
