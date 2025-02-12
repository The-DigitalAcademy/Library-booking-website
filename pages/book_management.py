import streamlit as st
import psycopg2
from database import get_db_connection

def fetch_books(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.id, b.title, a.author_name, c.category_name, b.cover_url, b.description
        FROM books b
        JOIN authors a ON b.author_id = a.author_id
        JOIN categories c ON b.category_id = c.category_id
        WHERE b.user_id = %s
    """, (user_id,))
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

def add_book(user_id, title, author_name, category_name, cover_url, description):
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
        INSERT INTO books (user_id, title, author_id, category_id, cover_url, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, title, author_id, category_id, cover_url, description))
    conn.commit()
    cur.close()
    conn.close()

def delete_book(id, user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id = %s AND user_id = %s", (id, user_id))
    conn.commit()
    cur.close()
    conn.close()

def update_book(id, user_id, title, author_name, category_name, cover_url, description):
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
        WHERE id = %s AND user_id = %s
    """, (title, author_id, category_id, cover_url, description, id, user_id))
    conn.commit()
    cur.close()
    conn.close()


st.set_page_config(page_title="Book Management", layout="wide")


if 'refresh' not in st.session_state:
    st.session_state.refresh = False


if 'user_id' not in st.session_state:
    st.error("Please log in to manage your books.")
else:
    user_id = st.session_state.user_id

    st.header("Add a Book")
    title = st.text_input("Title")
    author_name = st.text_input("Author Name")
    category_name = st.text_input("Category Name")
    cover_url = st.text_input("Cover URL")
    description = st.text_area("Description")
    
    if st.button("Add Book"):
        if not title or not author_name or not category_name or not cover_url or not description:
            st.error("Please fill in all fields.")
        else:
            add_book(user_id, title, author_name, category_name, cover_url, description)
            st.success(f"Book '{title}' added successfully!")
            st.session_state.refresh = True  
            st.rerun()  

    st.header("My Books")
    books = fetch_books(user_id)
    
    for index, book in enumerate(books):
        id, title, author, category_name, cover_url, description = book
        st.write(f"**Title:** {title}")
        st.write(f"**Author:** {author}")
        st.write(f"**Category:** {category_name}")
        st.write(f"**Description:** {description}")
        st.image(cover_url, width=150)

        # Update a book
        st.subheader("Update Book")
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

        # Delete a book
        if st.button(f"Delete {title}", key=f"delete_{id}_{index}"):
            delete_book(id, user_id)
            st.success(f"Book '{title}' deleted successfully!")
            st.session_state.refresh = True
            st.rerun()  
