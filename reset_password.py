import streamlit as st
import psycopg2

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="store_books",
        user="postgres",
        password="",  # Replace with actual password
        host="localhost"
    )

def reset_password(email, new_password):
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if email exists
    cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if user:
        cur.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, email))
        conn.commit()
        st.success("Password reset successful! You can now log in.")
        st.session_state.page = "Login"
        st.rerun()

    else:
        st.error("Email not found.")

    cur.close()
    conn.close()

def show_reset_password():
    st.title("Reset Password")

    email = st.text_input("Enter your email")
    new_password = st.text_input("Enter new password", type="password")

    if st.button("Reset Password"):
        if email and new_password:
            reset_password(email, new_password)
        else:
            st.error("Please fill in all fields.")
