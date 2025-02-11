

import psycopg2
import bcrypt
import re  # Import regex for email validation
import os  

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "events"),
        user=os.getenv("DB_USER", "dylan"),
        password=os.getenv("DB_PASSWORD", "super123duper"),  
        host=os.getenv("DB_HOST", "129.232.211.166")
    )

# Email validation function
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

# Function to create user
def create_user(username, email, password):
    if not is_valid_email(email):
        return "Invalid email format"
    
    if len(password) < 5:
        return "Password must be at least 5 characters long"
    
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cur.execute("INSERT INTO userz (username, email, password) VALUES (%s, %s, %s)", 
                    (username, email, hashed_pw))
        conn.commit()
        return "User created successfully"
    except psycopg2.IntegrityError:
        conn.rollback()  
        return "Username or email already exists"
    finally:
        cur.close()
        conn.close()

# Function to authenticate user (Only allows users who have signed up)
def authenticate_user(email, password):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT user_id, password FROM userz WHERE email = %s", (email,))
        user = cur.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            return user[0]  # Return user_id if authentication is successful
        return None
    finally:
        cur.close()
        conn.close()

# Function to reset password
def reset_password(email, new_password):
    if not is_valid_email(email):
        return "Invalid email format"
    
    if len(new_password) < 5:
        return "Password must be at least 5 characters long"
    
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cur.execute("UPDATE userz SET password = %s WHERE email = %s", 
                    (hashed_pw, email))
        conn.commit()
        return "Password reset successfully"
    except psycopg2.Error as e:
        conn.rollback()
        return f"Error resetting password: {e}"
    finally:
        cur.close()
        conn.close()