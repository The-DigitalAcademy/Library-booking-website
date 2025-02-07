import streamlit as st
from database import create_user
import re
from database import get_db_connection

def is_valid_email(email):
    """Check if the email is valid using regex."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

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

    # Check if email already exists
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cur.fetchone()
    if existing_user:
        st.error("Email already exists. Please use a different email.")
        return

    # Insert new user
    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password))

    conn.commit()
    cur.close()
    conn.close()
    
    st.success("Account created successfully! You can now log in.")

# Streamlit UI
st.title("Sign Up")

username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    if username and email and password:
        register_user(username, email, password)
    else:
        st.error("All fields are required!")

