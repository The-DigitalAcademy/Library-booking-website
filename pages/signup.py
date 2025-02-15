import streamlit as st
from database import get_db_connection
import bcrypt
import re

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

    # Determine role based on email
    if email.startswith("admin@"):  # Example: Emails ending with "@library.com" are admins
        role = "admin"
    else:
        role = "user"

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the email already exists
    cur.execute("SELECT * FROM userz WHERE email = %s", (email,))
    existing_user = cur.fetchone()
    if existing_user:
        st.error("Email already exists. Please use a different email.")
        return

    # Hash the password
    hashed_password = hash_password(password)

    # Insert the user into the database with the assigned role
    cur.execute("""
        INSERT INTO userz (username, email, password, role)
        VALUES (%s, %s, %s, %s)
    """, (username, email, hashed_password, role))

    conn.commit()
    cur.close()
    conn.close()
    
    st.success("Account created successfully! You can now log in.")

def show():
    """Displays the sign-up form in Streamlit."""
    st.title("Sign Up")

    username = st.text_input("Username", placeholder='nayna')
    email = st.text_input("Email", placeholder='nayna@gmail.com')
    password = st.text_input("Password", type="password", placeholder=12345)

    if st.button("Sign Up"):
        if username and email and password:
            register_user(username, email, password)
        else:
            st.error("All fields are required!")

if __name__ == "__main__":
    show()