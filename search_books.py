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

# Search books
def search_books(query):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.availability, b.title, a.author_name, b.book_id, b.category_id, b.cover_url, b.description
        FROM books b
        JOIN authors a ON b.author_id = a.author_id
        WHERE b.title ILIKE %s OR a.author_name ILIKE %s
    """, (f"%{query}%", f"%{query}%"))
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

# Streamlit interface
st.set_page_config(page_title="Malawi Library", layout="wide")

# Search books
st.header("Search Books")
query = st.text_input("Enter book title or author name")
if st.button("Search"):
    books = search_books(query)
    for book in books:
        availability, title, author, book_id, category_id, cover_url, description = book
        st.write(f"**Title:** {title}")
        st.write(f"**Author:** {author}")
        st.write(f"**Availability:** {'Available' if availability else 'Not Available'}")
        st.write(f"**Description:** {description}")