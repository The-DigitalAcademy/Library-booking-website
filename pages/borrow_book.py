import streamlit as st
import psycopg2
from datetime import date, timedelta
from database import get_db_connection

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

def borrow_book(book_id, user_id, collection_date, return_date):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, author_id FROM books 
        WHERE book_id = %s AND availability = TRUE 
        LIMIT 1
    """, (str(book_id),))
    book = cur.fetchone()

    if book:
        id, author_id = book 
        cur.execute("""
            INSERT INTO bookings (id, user_id, author_id, collection_date, return_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (id, user_id, author_id, collection_date, return_date))

        cur.execute("""
            UPDATE books SET availability = FALSE WHERE id = %s
        """, (id,))

        conn.commit()
        st.success(f"Book '{title}' borrowed successfully!")
    else:
        st.error("No available copies of this book.")

    cur.close()
    conn.close()


st.header("Available Books")
books = fetch_books()

user_id = st.session_state.get('user_id')
if not user_id:
    st.error("You must be logged in to borrow a book.")
else:
    for index, book in enumerate(books):
        availability, title, author, book_id, category_id, cover_url, description = book
        st.write(f"**Title:** {title}")
        st.write(f"**Author:** {author}")
        st.write(f"**Availability:** {'Available' if availability else 'Not Available'}")
        st.write(f"**Description:** {description}")
        st.image(cover_url, width=150) 
        
        if availability:
            collection_date = st.date_input(
                "Collection Date", 
                min_value=date.today(), 
                max_value=date.today() + timedelta(days=2), 
                key=f"collection_{user_id}_{book_id}_{index}"  
            )
            
            return_date = st.date_input(
                "Return Date", 
                min_value=date.today(), 
                max_value=collection_date + timedelta(days=30), 
                key=f"return_{user_id}_{book_id}_{index}" 
            )

            if st.button("Borrow", key=f"borrow_{user_id}_{book_id}_{index}"):
                if collection_date > date.today() + timedelta(days=2):
                    st.error("You have two days to collect the book after booking it.")
                elif return_date > collection_date + timedelta(days=30):
                    st.error("You cannot keep the book for more than a month.")
                else:
                    borrow_book(book_id, user_id, collection_date, return_date)


