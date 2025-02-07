import streamlit as st
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="events",
        user="dylan",
        password="super123duper",  # Replace with your actual password
        host="129.232.211.166"
    )

# Function to add a book
def add_book(title, author, category_id, cover_url, user_id, published_date, description):
    conn = get_db_connection()
    cur = conn.cursor()

     # Insert author if it doesn't exist
    cur.execute("INSERT INTO authors (author_name) VALUES (%s) ON CONFLICT (author_name) DO NOTHING RETURNING author_id", (author,))
    author_id = cur.fetchone()

    if not author_id:  # If author already exists, fetch their ID
        cur.execute("SELECT author_id FROM authors WHERE author_name = %s", (author,))
        author_id = cur.fetchone()[0]
    else:
        author_id = author_id[0]

# Insert book into the books table
    cur.execute("""
        INSERT INTO books (title, author_id, category_id, cover_url, user_id, published_date, availability, description)
        VALUES (%s, %s, %s, %s, %s, %s, TRUE, %s)
    """, (title, author_id, category_id, cover_url, user_id, published_date, description))

    conn.commit()
    cur.close()
    conn.close()
    st.success("Book added successfully!")
    
# Function to fetch books owned by the logged-in user
def fetch_user_books(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT book_id, title FROM books WHERE user_id = %s", (user_id,))
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

# Delete book function (only by owner)
def delete_book(book_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
    conn.commit()
    cur.close()
    conn.close()
    st.success("Book deleted successfully!")
    
    # Book a book (others can book available books)
def book_book(book_id, user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT availability FROM books WHERE book_id = %s", (book_id,))
    availability = cur.fetchone()[0]

    if availability:
        cur.execute("INSERT INTO bookings (book_id, user_id, booking_date, status) VALUES (%s, %s, CURRENT_DATE, 'booked')", (book_id, user_id))
        cur.execute("UPDATE books SET availability = FALSE WHERE book_id = %s", (book_id,))
        conn.commit()
        st.success("Book successfully booked!")
    else:
        st.warning("This book is already booked!")

    cur.close()
    conn.close()

# Show user books and allow management
def show_books():
    logged_in_user_id = st.session_state.get("user_id")

    if not logged_in_user_id:
        st.warning("You must be logged in to add or manage books.")
        return

    # Fetch user books
    user_books = fetch_user_books(logged_in_user_id)

    if user_books:
        st.subheader("Your Books")
        for book_id, title in user_books:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📖 {title}")
            with col2:
                if st.button("Delete", key=f"delete_{book_id}"):
                    delete_book(book_id)
                    
 # Book adding form
    st.subheader("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    category_id = st.number_input("Category ID", min_value=1)
    cover_url = st.text_input("Cover Image URL")
    published_date = st.date_input("Published Date")
    description = st.text_area("Description")

    if st.button("Add Book"):
        if title and author and cover_url:
            add_book(title, author, category_id, cover_url, logged_in_user_id, published_date, description)
        else:
            st.error("Please fill in all fields.")
            
    # Function to allow other users to browse and book books
def browse_books():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT book_id, title, availability FROM books")
    books = cur.fetchall()
    cur.close()
    conn.close()

    st.subheader("Browse Books")
    for book_id, title, availability in books:
        st.write(f"📖 {title} - {'Available' if availability else 'Not Available'}")
        if availability:
            if st.button(f"Book {title}", key=book_id):
                logged_in_user_id = st.session_state.get("user_id")
                if logged_in_user_id:
                    book_book(book_id, logged_in_user_id)
                else:
                    st.warning("You must be logged in to book a book.")
    
def show():
    st.title("Library Booking System")

    # Create a top navigation bar using columns
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("Home"):
            st.session_state.tab = "Home"

    with col2:
        if st.button("Add Book"):
            st.session_state.tab = "Add Book"

    with col3:
        if st.button("Profile"):
            st.session_state.tab = "Profile"

    with col4:
        if st.button("About Us"):
            st.session_state.tab = "About Us"

    with col5:
        if st.button("Logout"):
            st.session_state.page = "Login"  # Log out and go back to login
            st.rerun()


    # Display the selected tab's content
    if "tab" not in st.session_state:
        st.session_state.tab = "Home"  # Default tab is Home

    if st.session_state.tab == "Home":
        st.subheader("Welcome to the Library Booking System!")
        st.write("Search for books and manage your library.")

    elif st.session_state.tab == "Add Book":
        show_books()

    elif st.session_state.tab == "Profile":
        st.subheader("Your Profile")
        st.write("User profile details will be shown here.")

    elif st.session_state.tab == "About Us":
        st.subheader("About Us")
        st.write("This is a library booking system where users can search for books, add books, and manage their collections.")

