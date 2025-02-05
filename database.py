import psycopg2
import bcrypt

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="store_books",
        user="postgres",
        password="",
        host="localhost"
    )

# Function to create user
def create_user(username, email, password):
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                    (username, email, hashed_pw))
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        conn.rollback()  # Rollback in case of duplicate username/email
        return False
    finally:
        cur.close()
        conn.close()

# Function to authenticate user
def authenticate_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        return True
    return False
