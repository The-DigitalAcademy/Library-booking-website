import streamlit as st
import psycopg2
from datetime import date, timedelta
from database import get_db_connection

st.set_page_config(page_title="Malawi Library", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    header {visibility: hidden;} /* Hides the top menu bar */
    section[data-testid="stSidebarNav"] {display: none;} /* Hides the sidebar */
       .stApp {
            background-color: #FAF3E0;
        }
    .book-container {
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            text-align: center;
        }
        .book-header {
            color: #4CAF50;
            font-weight: bold;
            font-size: 18px;
            margin-top: 10px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        body {
            background-color: #f7f7f7;
            font-family: 'Arial', sans-serif;
        }
        .stTextInput, .stButton, .stError {
            border-radius: 10px;
            padding: 12px;
            margin: 8px 0;
        }
        .stTextInput input, .stDateInput input {
            border: 2px solid #ddd;
            padding: 10px;
            font-size: 16px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border: none;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            border-radius: 8px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stError {
            color: #f44336;
            font-weight: bold;
        }
        .stSuccess {
            color: #4CAF50;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

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
        st.success(f"Book '{book_id}' borrowed successfully!")
    else:
        st.error("No available copies of this book.")

    cur.close()
    conn.close()

# Show the available books and borrow form
st.header("Malawi Books")
books = fetch_books()

user_id = st.session_state.get('user_id')
if not user_id:
    st.error("You must be logged in to borrow a book.")
else:
    for index, book in enumerate(books):
        availability, title, author, book_id, category_id, cover_url, description = book
        short_description = (description[:200] + '...') if len(description) > 200 else description

        st.markdown(f"""
        <div class="book-container">
            <p class="book-header">{title} by {author}</p>
            <p><strong>Availability:</strong> {'Available' if availability else 'Not Available'}</p>
            <p><strong>Description:</strong> {short_description}</p>
            <img src="{cover_url}" width="150" style="border-radius: 8px; margin-bottom: 10px;" />
        </div>
        """, unsafe_allow_html=True)
        
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
