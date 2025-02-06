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
header_col1, header_col2 = st.columns([1, 3])
with header_col1:
    st.image("/Users/tshmacm1173/Desktop/Sprint3/Library-booking-website/MalawiLibraryLogo.jpg", width=100)  
    st.write("Malawi Library")
with header_col2:
    search_col, login_col, signup_col = st.columns([3, 1, 1])
    with search_col:
        st.text_input("Search Books")
    with login_col:
        st.button("Log In")
    with signup_col:
        st.button("Sign Up")

# Display genres and books
genres = fetch_genres()
books = fetch_books()

default_cover_url = "/Users/tshmacm1173/Desktop/Sprint3/Library-booking-website/coverpage.jpg"  # Replace with the path to your default cover image

for genre_id, genre_name in genres:
    st.subheader(genre_name)
    genre_books = [book for book in books if book[4] == genre_id]
    
    for index, book in enumerate(genre_books[:3]):  # Show only the first 3 books for each genre
        availability, title, author, book_id, _, cover_url = book
        book_col1, book_col2 = st.columns([1, 3])
        
        with book_col1:
            if cover_url == 'No cover' or not cover_url:
                st.image(default_cover_url, width=100)  # Use the default cover image
            else:
                st.image(cover_url, width=100)  # Fetch the cover URL from the database
        with book_col2:
            st.write("Available" if availability else "Not Available")
            st.write(f"**{title}**")
            st.write(f"by {author}")
            st.button("Borrow a book", key=f"{book_id}_{index}")