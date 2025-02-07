import streamlit as st
import psycopg2

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
def fetch_books(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.book_id, b.title, a.author_name, b.category_id, b.cover_url, b.description
        FROM books b
        JOIN authors a ON b.author_id = a.author_id
        WHERE b.user_id = %s
    """, (user_id,))
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

# Add a book
def add_book(user_id, title, author_id, category_id, cover_url, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO books (user_id, title, author_id, category_id, cover_url, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, title, author_id, category_id, cover_url, description))
    conn.commit()
    cur.close()
    conn.close()

# Delete a book
def delete_book(book_id, user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE book_id = %s AND user_id = %s", (book_id, user_id))
    conn.commit()
    cur.close()
    conn.close()

# Update a book
def update_book(book_id, user_id, title, author_id, category_id, cover_url, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE books
        SET title = %s, author_id = %s, category_id = %s, cover_url = %s, description = %s
        WHERE book_id = %s AND user_id = %s
    """, (title, author_id, category_id, cover_url, description, book_id, user_id))
    conn.commit()
    cur.close()
    conn.close()

# Streamlit interface
st.set_page_config(page_title="Book Management", layout="wide")

# User ID (replace with actual user authentication)
user_id = 1  # Replace with the actual user ID

# Add a book
st.header("Add a Book")
title = st.text_input("Title")
author_id = st.text_input("Author ID")
category_id = st.text_input("Category ID")
cover_url = st.text_input("Cover URL")
description = st.text_area("Description")
if st.button("Add Book"):
    add_book(user_id, title, author_id, category_id, cover_url, description)
    st.success(f"Book '{title}' added successfully!")

# Display user's books
st.header("Your Books")
books = fetch_books(user_id)
for book in books:
    book_id, title, author, category_id, cover_url, description = book
    st.write(f"**Title:** {title}")
    st.write(f"**Author:** {author}")
    st.write(f"**Category ID:** {category_id}")
    st.write(f"**Description:** {description}")
    st.image(cover_url, width=150)  # Display the book cover

    # Update a book
    st.subheader("Update Book")
    new_title = st.text_input(f"New Title for {title}", value=title)
    new_author_id = st.text_input(f"New Author ID for {title}", value=author_id)
    new_category_id = st.text_input(f"New Category ID for {title}", value=category_id)
    new_cover_url = st.text_input(f"New Cover URL for {title}", value=cover_url)
    new_description = st.text_area(f"New Description for {title}", value=description)
    if st.button(f"Update {title}"):
        update_book(book_id, user_id, new_title, new_author_id, new_category_id, new_cover_url, new_description)
        st.success(f"Book '{new_title}' updated successfully!")

    # Delete a book
    if st.button(f"Delete {title}"):
        delete_book(book_id, user_id)
        st.success(f"Book '{title}' deleted successfully!")