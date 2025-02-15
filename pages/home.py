import streamlit as st
import psycopg2
from database import get_db_connection
from streamlit_extras.switch_page_button import switch_page

# Page configuration
st.set_page_config(page_title="Malawi Library", layout="wide", initial_sidebar_state="collapsed")

hide_sidebar_style = """
<style>
.st-emotion-cache-19u4bdk.eczjsme5 {
    display: none;
}
</style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
    <style>
        /* General page styling */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            display-content: center;
        }

        /* Background color for the whole page */
        .stApp {
            background-color: #FAF3E0;
        }

        /* Navigation tabs */
        .tabs-container {
            display: flex;
            justify-content: center;
            gap: 5px;
            margin-bottom: 10px;
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
            width: 250px;
            text-align: center;
            padding: 15px;
            background-color: #f4f4f4;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            transition: transform 0.3s ease-in-out;
            animation: sliding 3s ease-in-out infinite alternate;
        }

        /* Hover effect - book moves up slightly */
        .book-container:hover {
            transform: translateY(-10px);
        }

        /* Book image styling */
        .book-details img {
            border-radius: 5px;
        }

        /* Book availability styling */
        .availability {
            background-color: brown;
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 5px;
            color: white;
            padding: 2px;
            border-radius: 5px;
            text-align: center;
        }

        /* Sliding animation - books move left and right */
        @keyframes sliding {
            0% { transform: translateX(0); }
            100% { transform: translateX(20px); }
        }
    </style>
""", unsafe_allow_html=True)

# Navigation bar
st.markdown('<div class="tabs-container">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
   st.subheader("📖 Welcome to the Malawi Booking Books System!")
   st.write("Search for books, borrow them, and manage your library collection")

with col2:
    if st.button("🚪 Logout", key="logout"):
        switch_page("login")

st.markdown('</div>', unsafe_allow_html=True)

# Search bar
st.markdown(
    """
    <style>
        .search-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
        }

        .stTextInput>div>div>input {
            padding: 10px;
            font-size: 16px;
            border: 2px solid #f1c40f;
            border-radius: 8px;
            width: 6000px;
            background-color: white;
            color: white;
        }

        .stButton>button {
            background-color: #f1c40f;
            color: black;
            font-size: 16px;
            padding: 8px 16px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: 0.3s;
        }

        .stButton>button:hover {
            background-color: #e67e22;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="search-container">', unsafe_allow_html=True)
query = st.text_input("🔍 Search Books", key="search_input")
search_button = st.button("Search", key="search_btn")
st.markdown('</div>', unsafe_allow_html=True)

# Fetch books and genres from the database
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

# Filter books based on search query
if search_button and query:
    books = [book for book in books if query.lower() in book[1].lower()]

default_cover_url = "assets/coverpage.jpg"

# Display books by genre
for genre_id, genre_name in genres:
    st.markdown(f"<h2>{genre_name}</h2><hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)
    genre_books = [book for book in books if book[4] == genre_id]
    
    if not genre_books:
        st.write("No books available in this category.")

    # Display 6 books per category
    book_cols = st.columns(3)  # 3 columns per row
    for index, book in enumerate(genre_books[:6]):  # Display up to 6 books
        availability, title, author, book_id, _, cover_url, description = book
        with book_cols[index % 3]:  # Cycle through columns
            st.markdown(
                f"""
                <div class="book-container">
                    <div class="availability">
                        {"✅ Available" if availability else "❌ Not Available"}
                    </div>
                    <div class="book-details">
                        <img src="{cover_url if cover_url != 'No cover' else default_cover_url}" width="150">
                    </div>
                    <div>
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

            # Display Borrow button only if the book is available
            if availability:
                if st.button("Borrow", key=f"{genre_id}_{id}_{index}"):
                    st.session_state["selected_book"] = id
                    switch_page('borrow_book')

# Footer
st.markdown(
    """
    <style>
        .footer-container {
            background-color: #2c3e50; /* Dark background for contrast */
            color: white; /* White text for readability */
            padding: 20px;
            border-radius: 10px;
            margin-top: 50px;
            text-align: center;
        }

        .footer-container h3 {
            color: #f1c40f; /* Highlighted text color */
            margin-bottom: 10px;
        }

        .footer-columns {
            display: flex;
            justify-content: space-between;
            gap: 40px;
            padding: 10px 50px;
        }

        .footer-section {
            flex: 1;
            min-width: 200px;
        }

        .footer-container a {
            color: #f1c40f;
            text-decoration: none;
            font-weight: bold;
        }

        .footer-container a:hover {
            color: #e67e22; /* Different color on hover */
        }

        hr {
            border: none;
            height: 2px;
            background: #f1c40f;
            margin: 20px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="footer-container">', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="footer-columns">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="footer-section">', unsafe_allow_html=True)
        st.subheader("📌 About Us")
        st.write("Malawi Library is an innovative book booking system where users can explore, reserve, and manage books with ease.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="footer-section">', unsafe_allow_html=True)
        st.subheader("📞 Contact Us")
        st.write("✉️ Email: [contact@malawilibrary.com](mailto:contact@malawilibrary.com)")
        st.write("📞 Phone: +123 456 7890")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="footer-section">', unsafe_allow_html=True)
        st.subheader("📍 Location")
        st.write("🏢 123 Library Street, Johannesburg, South Africa")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)