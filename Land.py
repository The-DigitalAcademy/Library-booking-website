import streamlit as st
import requests
import psycopg2

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname="store_books",
        user="postgres",
        password="",  # Replace with your actual password
        host="localhost"
    )
    return conn

# Fetch books from the database
def fetch_books():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.availability, b.title, a.authors_name, b.book_id, b.category_id, b.cover_url
        FROM books b
        JOIN authors a ON b.author_id = a.author_id
    """)
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

# Fetch genres from the database
def fetch_genres():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, category_name FROM categories")
    genres = cur.fetchall()
    cur.close()
    conn.close()
    return genres

# Streamlit interface
st.set_page_config(page_title="Malawi Library", layout="wide")

# Logo and title
col1, col2 = st.columns([1, 3])
with col1:
    st.image("/Users/tshmacm1173/Downloads/shunya-koide-1emWndlDHs0-unsplash.jpg", width=250)  # Replace with the path to your logo image
with col2:
    st.title("Malawi Library")

# Top right buttons
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.text_input("Search Books")
with col2:
    st.button("Log In")
with col3:
    st.button("Sign Up")

# Display genres and books
genres = fetch_genres()
books = fetch_books()

for genre_id, genre_name in genres:
    st.subheader(genre_name)
    genre_books = [book for book in books if book[4] == genre_id]
    
    for book in genre_books:
        availability, title, author, book_id, _, cover_url = book
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.image(cover_url, width=100)  # Fetch the cover URL from the database
        with col2:
            st.write(f"**{title}**")
            st.write(f"by {author}")
            st.write("Available" if availability else "Not Available")
        with col3:
            st.button("View Book", key=book_id)

# Note: Ensure that the `cover_url` column exists in your `books` table and contains the URL of the book cover images.