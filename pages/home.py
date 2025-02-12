import streamlit as st
import psycopg2
from database import get_db_connection
from streamlit_extras.switch_page_button import switch_page

# Page config for wide layout
st.set_page_config(page_title="Malawi Library", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        /* General page styling */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
        }
         /* Background color for the whole page */
        .stApp {
            background-color: paige;
        }
        /* Navigation tabs */
        .tabs-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        .tab-button {
            background-color: #2c3e50;
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            cursor: pointer;
            text-align: center;
            transition: 0.3s;
            font-weight: bold;
        }
        .tab-button:hover {
            background-color: #34495e;
        }

        /* Book containers */
        .book-container {
            text-align: center;
            padding: 15px;
            background-color: #ecf0f1;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .book-details img {
            border-radius: 5px;
        }
        .availability {
            font-size: 14px;
            font-weight: bold;
            color: #16a085;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Navigation Tabs
st.markdown('<div class="tabs-container">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 Home", key="home"):
        switch_page("home")

with col2:
    if st.button("📚 Add Book", key="add_book"):
        switch_page("book_management")

with col3:
    if st.button("👤 Profile", key="profile"):
        switch_page("user_profile")

with col4:
    if st.button("🚪 Logout", key="logout"):
        switch_page("login")

st.markdown('</div>', unsafe_allow_html=True)

# Home Page Content
st.subheader("📖 Welcome to the Malawi Library Booking System!")
st.write("Search for books, borrow them, and manage your library collection.")

query = st.text_input("🔍 Search Books")
search_button = st.button("Search")

# Fetch books & genres from the database
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

def fetch_genres():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, category_name FROM categories")
    genres = cur.fetchall()
    cur.close()
    conn.close()
    return genres

books = fetch_books()
genres = fetch_genres()

# Search Filter
if search_button and query:
    books = [book for book in books if query.lower() in book[1].lower()]

default_cover_url = "assets/coverpage.jpg"

# Display Books by Genre
for genre_id, genre_name in genres:
    st.subheader(f"📚 {genre_name}")
    genre_books = [book for book in books if book[4] == genre_id]
    
    if not genre_books:
        st.write("No books available in this category.")

    # Display books in a row format
    book_cols = st.columns(3)
    for index, book in enumerate(genre_books[:3]):
        availability, title, author, book_id, _, cover_url, description = book
        with book_cols[index]:
            st.markdown(
                f"""
                <div class="book-container">
                    <div class="availability">
                        {"✅ Available" if availability else "❌ Not Available"}
                    </div>
                    <div class="book-details">
                        <img src="{cover_url if cover_url != 'No cover' else default_cover_url}" width="150">
                        <strong>{title}</strong><br>
                        <em>by {author}</em>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.expander("📖 Show Description"):
                 summary = description[:200] + "..." if len(description) > 200 else description
                 st.write(summary)

            if st.button("Borrow", key=f"{book_id}_{index}"):
                switch_page('borrow_book') 

# Footer Section
st.markdown("<hr>", unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📌 About Us")
        st.write("Malawi Library is an innovative book booking system where users can explore, reserve, and manage books with ease.")

    with col2:
        st.subheader("📞 Contact Us")
        st.write("✉️ Email: contact@malawilibrary.com")
        st.write("📞 Phone: +123 456 7890")

    with col3:
        st.subheader("📍 Location")
        st.write("🏢 123 Library Street, Johannesburg, South Africa")
