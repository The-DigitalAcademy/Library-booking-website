# import streamlit as st
# import requests
# import psycopg2

# # Database connection
# def get_db_connection():
#     conn = psycopg2.connect(
#         dbname="events",
#         user="dylan",
#         password="super123duper",  # Replace with your actual password
#         host="129.232.211.166"
#     )
#     return conn

# # Fetch books from the database
# def fetch_books():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT b.availability, b.title, a.author_name, b.book_id, b.category_id, b.cover_url, b.description
#         FROM books b
#         JOIN authors a ON b.author_id = a.author_id
#     """)
#     books = cur.fetchall()
#     cur.close()
#     conn.close()
#     return books

# # Fetch genres from the database
# def fetch_genres():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT category_id, category_name FROM categories")
#     genres = cur.fetchall()
#     cur.close()
#     conn.close()
#     return genres

# # Streamlit interface
# st.set_page_config(page_title="Malawi Library", layout="wide")

# # Custom CSS for styling
# st.markdown(
#     """
#     <style>
#     .header-title {
#         font-size: 32px;
#         font-weight: bold;
#     }
#     .header-buttons {
#         display: flex;
#         justify-content: flex-end;
#         gap: 10px;
#     }
#     .book-container {
#         box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
#         padding: 10px;
#         border-radius: 5px;
#     }
#     .availability {
#         background-color: brown;
#         color: white;
#         padding: 5px;
#         border-radius: 5px;
#         text-align: center;
#     }
#     .book-details {
#         text-align: center;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Logo and title
# header_col1, header_col2 = st.columns([1, 3])
# with header_col1:
#     st.image("assets/MalawiLibraryLogo.jpg", width=200)  # Corrected path
#     st.markdown('<div class="header-title">Malawi Library</div>', unsafe_allow_html=True)
# with header_col2:
#     st.markdown(
#         """
#         <div class="header-buttons">
#             <input type="text" placeholder="Search Books" style="padding: 5px; font-size: 16px;">
#             <button style="padding: 5px 10px; font-size: 16px;">Log In</button>
#             <button style="padding: 5px 10px; font-size: 16px;">Sign Up</button>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# # Display genres and books
# genres = fetch_genres()
# books = fetch_books()

# default_cover_url = "assets/coverpage.jpg"  # Corrected path

# for genre_id, genre_name in genres:
#     st.subheader(genre_name)
#     genre_books = [book for book in books if book[4] == genre_id]
    
#     book_cols = st.columns(3)  # Create 3 columns for books
#     for index, book in enumerate(genre_books[:3]):  # Show only the first 3 books for each genre
#         availability, title, author, book_id, _, cover_url, description = book
        
#         with book_cols[index]:
#             st.markdown(
#                 f"""
#                 <div class="book-container">
#                     <div class="availability">
#                         {"Available" if availability else "Not Available"}
#                     </div>
#                     <div class="book-details">
#                         <img src="{cover_url if cover_url != 'No cover' else default_cover_url}" width="200">
#                         <strong>{title}</strong><br>
#                         by {author}
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
#             with st.expander("Show Description"):
#                 st.write(description)
#             st.button("Borrow a book", key=f"{book_id}_{index}")



import streamlit as st
import requests
import psycopg2
from streamlit_extras.switch_page_button import switch_page


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

# Fetch genres from the database
def fetch_genres():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, category_name FROM categories")
    genres = cur.fetchall()
    cur.close()
    conn.close()
    return genres

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

# Custom CSS for styling
st.markdown(
    """
    <style>
    .header-title {
        font-size: 32px;
        font-weight: bold;
    }
    .header-buttons {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
    }
    .book-container {
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        padding: 10px;
        border-radius: 5px;
    }
    .availability {
        background-color: brown;
        color: white;
        padding: 5px;
        border-radius: 5px;
        text-align: center;
    }
    .book-details {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logo and title
header_col1, header_col2 = st.columns([1, 3])
with header_col1:
    st.image("assets/MalawiLibraryLogo.jpg", width=200)  # Corrected path
    st.markdown('<div class="header-title">Malawi Library</div>', unsafe_allow_html=True)
with header_col2:
    search_col, login_col, signup_col = st.columns([3, 1, 1])
    with search_col:
        query = st.text_input("Search Books")
        search_button = st.button("Search")
    # with login_col:
    #     st.button("Log In")
    # with signup_col:
    #     st.button("Sign Up"

with login_col:
    if st.button("Log In"):
        switch_page('login')

with signup_col :
    if st.button("Sign Up"):
        switch_page('signup')

# Display genres and books
genres = fetch_genres()
books = fetch_books()

if search_button and query:
    books = search_books(query)

default_cover_url = "assets/coverpage.jpg"  # Corrected path

for genre_id, genre_name in genres:
    st.subheader(genre_name)
    genre_books = [book for book in books if book[4] == genre_id]
    
    book_cols = st.columns(3)  # Create 3 columns for books
    for index, book in enumerate(genre_books[:3]):  # Show only the first 3 books for each genre
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