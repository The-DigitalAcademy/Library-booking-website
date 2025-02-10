

import streamlit as st
import psycopg2
from datetime import date, timedelta


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
def borrow_book(book_id, user_id, collection_date, return_date):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bookings (id, user_id, author_id, collection_date, return_date)
        SELECT b.id, %s, b.author_id, %s, %s
        FROM books b
        WHERE b.book_id = %s
    """, (user_id, collection_date, return_date, book_id))
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
    st.image(cover_url, width=150)  # Display the book cover
    
    if availability:
        collection_date = st.date_input("Collection Date", min_value=date.today(), max_value=date.today() + timedelta(days=2), key=f"collection_{book_id}")
        return_date = st.date_input("Return Date", min_value=date.today(), max_value=date.today() + timedelta(days=30), key=f"return_{book_id}")
        
        if st.button("Borrow", key=book_id):
            user_id = 1  # Replace with the actual user ID
            if collection_date > date.today() + timedelta(days=2):
                st.error("You have two days to collect the book after booking it.")
            elif return_date > collection_date + timedelta(days=30):
                st.error("You cannot keep the book for more than a month.")
            else:
                borrow_book(book_id, user_id, collection_date, return_date)
                st.success(f"Book '{title}' borrowed successfully!")