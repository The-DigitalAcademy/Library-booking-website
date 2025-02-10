import streamlit as st
import psycopg2
from database import get_db_connection
from book_management import add_book, fetch_books  # Import the necessary functions

st.set_page_config(page_title="Malawi Library", layout="wide")

# Sidebar Navigation
st.sidebar.image("assets/MalawiLibraryLogo.jpg", width=150)
st.sidebar.markdown("## Malawi Library")

# Sidebar Navigation Buttons
tab = st.sidebar.radio("Navigation", ["Home", "Add Book", "Profile", "Logout"])

# Handle Logout
if tab == "Logout":
    st.session_state.page = "Login"
    st.experimental_rerun()

# Page Content
if tab == "Home":
    st.subheader("Welcome to the Library Booking System!")
    st.write("Search for books and manage your library.")

    # Search Bar
    query = st.text_input("Search Books")
    search_button = st.button("Search")

    # Fetch books and genres
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

    if search_button and query:
        books = [book for book in books if query.lower() in book[1].lower()]

    default_cover_url = "assets/coverpage.jpg"

    for genre_id, genre_name in genres:
        st.subheader(genre_name)
        genre_books = [book for book in books if book[4] == genre_id]
        book_cols = st.columns(3)
        for index, book in enumerate(genre_books[:3]):
            availability, title, author, book_id, _, cover_url, description = book
            with book_cols[index]:
                st.markdown(
                    f"""
                    <div class="book-container">
                        <div class="availability">
                            {"Available" if availability else "Not Available"}
                        </div>
                        <div class="book-details">
                            <img src="{cover_url if cover_url != 'No cover' else default_cover_url}" width="200">
                            <strong>{title}</strong><br>
                            by {author}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                with st.expander("Show Description"):
                    st.write(description)
                st.button("Borrow a book", key=f"{book_id}_{index}")

elif tab == "Add Book":
    st.subheader("Add a Book")
    user_id = 1  
    title = st.text_input("Title")
    author_name = st.text_input("Author Name")
    category_name = st.text_input("Category Name")
    cover_url = st.text_input("Cover URL")
    description = st.text_area("Description")
    if st.button("Add Book"):
        add_book(user_id, title, author_name, category_name, cover_url, description)
        st.success(f"Book '{title}' added successfully!")

elif tab == "Profile":
    st.subheader("Your Profile")
    st.write("User profile details will be shown here.")

st.markdown("<hr>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("About Us")
    st.write("This is a library booking system where users can search for books, add books, and manage their collections.")
    
with col2:
    st.subheader("Contact Us")
    st.write("Email: contact@malawilibrary.com")
    st.write("Phone: +123 456 7890")
    
with col3:
    st.subheader("Location")
    st.write("123 Library Street, City, Country")