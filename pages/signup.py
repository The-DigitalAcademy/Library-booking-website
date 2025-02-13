

import streamlit as st
from database import get_db_connection
import bcrypt
import re
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
        .stButton>button:hover {
            background-color: #45a049;
        }
        h1 {
            text-align: center;
            color: #4CAF50;
            margin-bottom: 20px;
        }
        .stError {
            color: #f44336;
            font-weight: bold;
        }
        .stSuccess {
            color: #4CAF50;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-container">', unsafe_allow_html=True)
st.subheader("📖 Malawi Booking Books System!")
def is_valid_email(email):
    """Check if the email is valid using regex."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def hash_password(password):
    """Hash the password before storing it in the database."""
    salt = bcrypt.gensalt()  
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  
    return hashed_password.decode('utf-8') 

def register_user(username, email, password):
    """Registers a user if the email is valid and password meets the criteria."""
    if not is_valid_email(email):
        st.error("Invalid email! Please enter a valid email address.")
        return

    if len(password) < 5:
        st.error("Password must be at least 5 characters long.")
        return

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM userz WHERE email = %s", (email,))
    existing_user = cur.fetchone()
    if existing_user:
        st.error("Email already exists. Please use a different email.")
        return

    hashed_password = hash_password(password)

    cur.execute("INSERT INTO userz (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password))

    conn.commit()
    cur.close()
    conn.close()
    
    st.success("Account created successfully! You can now log in.")

def show():
    """Displays the sign-up form in Streamlit."""
    st.title("Sign Up")

    username = st.text_input("Username", placeholder="Enter your username")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Sign Up"):
        if username and email and password:
            register_user(username, email, password)
        else:
            st.error("All fields are required!")
st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show()