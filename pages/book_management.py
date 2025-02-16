import streamlit as st
import psycopg2
import uuid
from database import get_db_connection

st.set_page_config(page_title="Malawi Library", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS for styling
st.markdown("""
    <style>
    header {visibility: hidden;} /* Hides the top menu bar */
    section[data-testid="stSidebarNav"] {display: none;} /* Hides the sidebar */
       .stApp {
            background-color: #FAF3E0;
        }
        .book-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .book-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .book-cover {
            border-radius: 10px;
            width: 150px;  /* Adjust cover size */
            height: auto;
            margin-bottom: 15px;
        }
        .book-title {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .book-author, .book-category {
            font-size: 18px;
            color: #7f8c8d;
            margin-bottom: 10px;
        }
        .book-description {
            font-size: 16px;
            color: #34495e;
            margin-bottom: 15px;
        }
        .stButton button {
            background-color: #3498db;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.2s;
        }
        .stButton button:hover {
            background-color: #2980b9;
        }
        .stTextInput input, .stTextArea textarea {
            border: 2px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #3498db;
            outline: none;
        }
        .stHeader {
            color: #2c3e50;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .stSubheader {
            color: #34495e;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Function to check if the user is an admin
def is_admin(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT role FROM userz WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user and user[0]  # Return True if the user is an admin, otherwise False

# Function to fetch books (only for admins or the user's own books)
def fetch_books(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    if is_admin(user_id):
        # Admins can see all books
        cur.execute("""
            SELECT b.id, b.book_id, b.title, a.author_name, c.category_name, b.cover_url, b.description
            FROM books b
            JOIN authors a ON b.author_id = a.author_id
            JOIN categories c ON b.category_id = c.category_id
        """)
    else:
        # Non-admins can only see their own books
        cur.execute("""
            SELECT b.id, b.book_id, b.title, a.author_name, c.category_name, b.cover_url, b.description
            FROM books b
            JOIN authors a ON b.author_id = a.author_id
            JOIN categories c ON b.category_id = c.category_id
            WHERE b.user_id = %s
        """, (user_id,))
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

# Function to add a book (only for admins)
def add_book(user_id, title, author_name, category_name, cover_url, description):
    if not is_admin(user_id):
        st.error("You do not have permission to add books.")
        return

    conn = get_db_connection()
    cur = conn.cursor()
    book_id = str(uuid.uuid4())

    cur.execute("SELECT author_id FROM authors WHERE author_name = %s", (author_name,))
    author = cur.fetchone()
    if author is None:
        cur.execute("INSERT INTO authors (author_name) VALUES (%s) RETURNING author_id", (author_name,))
        author_id = cur.fetchone()[0]
    else:
        author_id = author[0]

    cur.execute("SELECT category_id FROM categories WHERE category_name = %s", (category_name,))
    category = cur.fetchone()
    if category is None:
        cur.execute("INSERT INTO categories (category_name) VALUES (%s) RETURNING category_id", (category_name,))
        category_id = cur.fetchone()[0]
    else:
        category_id = category[0]

    cur.execute("""
        INSERT INTO books (book_id, user_id, title, author_id, category_id, cover_url, description, availability)
        VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
    """, (book_id, user_id, title, author_id, category_id, cover_url, description))
    conn.commit()
    cur.close()
    conn.close()

# Function to delete a book (only for admins)
def delete_book(id, user_id):
    if not is_admin(user_id):
        st.error("You do not have permission to delete books.")
        return

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()

# Function to update a book (only for admins)
def update_book(id, user_id, title, author_name, category_name, cover_url, description):
    if not is_admin(user_id):
        st.error("You do not have permission to update books.")
        return

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT author_id FROM authors WHERE author_name = %s", (author_name,))
    author = cur.fetchone()
    if author is None:
        cur.execute("INSERT INTO authors (author_name) VALUES (%s) RETURNING author_id", (author_name,))
        author_id = cur.fetchone()[0]
    else:
        author_id = author[0]

    cur.execute("SELECT category_id FROM categories WHERE category_name = %s", (category_name,))
    category = cur.fetchone()
    if category is None:
        cur.execute("INSERT INTO categories (category_name) VALUES (%s) RETURNING category_id", (category_name,))
        category_id = cur.fetchone()[0]
    else:
        category_id = category[0]

    cur.execute("""
        UPDATE books
        SET title = %s, author_id = %s, category_id = %s, cover_url = %s, description = %s
        WHERE id = %s
    """, (title, author_id, category_id, cover_url, description, id))
    conn.commit()
    cur.close()
    conn.close()


if 'refresh' not in st.session_state:
    st.session_state.refresh = False

if 'user_id' not in st.session_state:
    st.error("Please log in to manage your books.")
else:
    user_id = st.session_state.user_id

    # Only admins can add books
    if is_admin(user_id):
        st.header("📚 Add a Book")
        title = st.text_input("Title", placeholder="Enter book title")
        author_name = st.text_input("Author Name", placeholder="Enter author name")
        category_name = st.text_input("Category Name", placeholder="Enter category name")
        cover_url = st.text_input("Cover URL", placeholder="Enter cover image URL")
        description = st.text_area("Description", placeholder="Enter book description")

        if st.button("Add Book"):
            if not title or not author_name or not category_name or not cover_url or not description:
                st.error("Please fill in all fields.")
            else:
                add_book(user_id, title, author_name, category_name, cover_url, description)
                st.success(f"Book '{title}' added successfully!")
                st.session_state.refresh = True
                st.rerun()

    st.header("📖 Malawi Books")
    books = fetch_books(user_id)

    for index, book in enumerate(books):
        id, book_id, title, author, category_name, cover_url, description = book
        short_description = (description[:200] + '...') if len(description) > 200 else description
        st.markdown(f"""
            <div class="book-card">
                <img src="{cover_url}" class="book-cover" alt="{title}">
                <div class="book-title">{title}</div>
                <div class="book-author">By {author}</div>
                <div class="book-category">Category: {category_name}</div>
                <div class="book-description">{short_description}</div>
            </div>
        """, unsafe_allow_html=True)

        # Only admins can update or delete books
        if is_admin(user_id):
            st.subheader("✏️ Update Book")
            new_title = st.text_input(f"New Title for {title}", value=title, key=f"new_title_{id}_{index}")
            new_author_name = st.text_input(f"New Author Name for {title}", value=author, key=f"new_author_{id}_{index}")
            new_category_name = st.text_input(f"New Category Name for {title}", value=category_name, key=f"new_category_{id}_{index}")
            new_cover_url = st.text_input(f"New Cover URL for {title}", value=cover_url, key=f"new_cover_{id}_{index}")
            new_description = st.text_area(f"New Description for {title}", value=description, key=f"new_description_{id}_{index}")

            if st.button(f"Update {title}", key=f"update_{id}_{index}"):
                update_book(id, user_id, new_title, new_author_name, new_category_name, new_cover_url, new_description)
                st.success(f"Book '{new_title}' updated successfully!")
                st.session_state.refresh = True
                st.rerun()

            if st.button(f"Delete {title}", key=f"delete_{id}_{index}"):
                delete_book(id, user_id)
                st.success(f"Book '{title}' deleted successfully!")
                st.session_state.refresh = True
                st.rerun()