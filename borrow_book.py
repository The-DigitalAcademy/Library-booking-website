import streamlit as st
import psycopg2

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname="events",
        user="dylan",
        password="super123duper",  # Replace with your actual password
        host="129.232.211.166"
    )
    return conn

# Fetch books from the database
def fetch_books():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.availability, b.title, a.author_name, b.book_id, b.category_id, b.cover_url, b.description
        FROM books b
        JOIN authors a ON b.author_id = a.author_id
    """)
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

# Borrow a book
def borrow_book(book_id, user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bookings (id, user_id, author_id)
        SELECT b.id, %s, b.author_id
        FROM books b
        WHERE b.book_id = %s
    """, (user_id, book_id))
    conn.commit()
    cur.close()
    conn.close()

# Streamlit interface
st.set_page_config(page_title="Borrow a Book", layout="wide")

# Display books
st.header("Available Books")
books = fetch_books()
for book in books:
    availability, title, author, book_id, category_id, cover_url, description = book
    st.write(f"**Title:** {title}")
    st.write(f"**Author:** {author}")
    st.write(f"**Availability:** {'Available' if availability else 'Not Available'}")
    st.write(f"**Description:** {description}")
    if st.button("Borrow", key=book_id):
        user_id = 1  # Replace with the actual user ID
        borrow_book(book_id, user_id)
        st.success(f"Book '{title}' borrowed successfully!")