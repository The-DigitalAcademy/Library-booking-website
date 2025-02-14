import streamlit as st
import requests
import psycopg2
from streamlit_extras.switch_page_button import switch_page
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

def fetch_genres():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, category_name FROM categories")
    genres = cur.fetchall()
    cur.close()
    conn.close()
    return genres

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

st.set_page_config(page_title="Malawi Library", layout="wide", initial_sidebar_state="collapsed")

hide_sidebar_style = """
<style>
.st-emotion-cache-19u4bdk.eczjsme5 {
    display: none;
}
</style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

st.markdown(
    """
    <style>
     /* General page styling */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            display-content: center
        }
         /* Background color for the whole page */
        .stApp {
            background-color: #FAF3E0;
        }
    .header-title {
        font-size: 20px;
        font-weight: lighter;
        font-style: oblique;
    }
    .header-buttons {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
    }
    .book-container {
        width: 300px;
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
     /* Sliding animation - books move left and right */
        @keyframes sliding {
            0% { transform: translateX(0); }
            100% { transform: translateX(20px); }
        }
    </style>
    """,
    unsafe_allow_html=True
)

header_col1, header_col2 = st.columns([1, 3])
with header_col1:
    st.image("assets/MalawiLibraryLogo.jpg", width= 100)  
    st.markdown('<div class="header-title">📖 Malawi Library</div>', unsafe_allow_html=True)
with header_col2:
    search_col, login_col, signup_col = st.columns([3, 1, 1])
    with search_col:
        query = st.text_input("Search Books")
        search_button = st.button("Search")
        
st.markdown('<div class="butt-container">', unsafe_allow_html=True)
with login_col:
    if st.button("Log In"):
        switch_page('login')

with signup_col :
    if st.button("Sign Up"):
        switch_page('signup')
st.markdown('</div>', unsafe_allow_html=True)   


# st.markdown(
#     """
#     <style>
#         .search-container {
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             gap: 10px;
#             margin-bottom: 20px;
#         }

#         .stTextInput>div>div>input {
#             padding: 10px;
#             font-size: 16px;
#             border: 2px solid #f1c40f;
#             border-radius: 8px;
#             width: 6000px;
#             background-color: #2c3e50;
#             color: white;
#         }

#         .stButton>button {
#             background-color: #f1c40f;
#             color: black;
#             font-size: 16px;
#             padding: 8px 16px;
#             border-radius: 8px;
#             border: none;
#             cursor: pointer;
#             transition: 0.3s;
#         }

#         .stButton>button:hover {
#             background-color: #e67e22;
#             color: white;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )  

genres = fetch_genres()
books = fetch_books()

if search_button and query:
    books = search_books(query)

default_cover_url = "assets/coverpage.jpg" 

for genre_id, genre_name in genres:
    
    st.markdown(f"<h2>{genre_name}</h2><hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)
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
                    </div>
                    <div>
                        <strong>{title}</strong><br>
                        by {author}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.expander("Show Description"):
                     summary = description[:200] + "..." if len(description) > 200 else description
                     st.write(summary)
            st.button("Borrow", key=f"{genre_id}_{book_id}_{index}")
   

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


# import streamlit as st
# import requests
# import psycopg2
# from streamlit_extras.switch_page_button import switch_page
# from database import get_db_connection

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

# def fetch_genres():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT category_id, category_name FROM categories")
#     genres = cur.fetchall()
#     cur.close()
#     conn.close()
#     return genres

# def search_books(query):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT b.availability, b.title, a.author_name, b.book_id, b.category_id, b.cover_url, b.description
#         FROM books b
#         JOIN authors a ON b.author_id = a.author_id
#         WHERE b.title ILIKE %s OR a.author_name ILIKE %s
#     """, (f"%{query}%", f"%{query}%"))
#     books = cur.fetchall()
#     cur.close()
#     conn.close()
#     return books

# st.set_page_config(page_title="Malawi Library", layout="wide", initial_sidebar_state="collapsed")

# hide_sidebar_style = """
# <style>
# .st-emotion-cache-19u4bdk.eczjsme5 {
#     display: none;
# }
# </style>
# """
# st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# st.markdown(
#     """
#     <style>
#      /* General page styling */
#         body {
#             font-family: 'Arial', sans-serif;
#             background-color: #f4f4f4;
#             display-content: center
#         }
#          /* Background color for the whole page */
#         .stApp {
#             background-color: #FAF3E0;
#         }
#     .header-title {
#         font-size: 20px;
#         font-weight: lighter;
#         font-style: oblique;
#     }
#     .header-buttons {
#         display: flex;
#         justify-content: flex-end;
#         gap: 10px;
#     }
#     .book-container {
#         width: 300px;
#         text-align: center;
#         padding: 15px;
#         background-color: #f4f4f4;
#         border-radius: 10px;
#         box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
#         margin-bottom: 20px;
#         transition: transform 0.3s ease-in-out;
#         animation: sliding 3s ease-in-out infinite alternate;
#     }
#      /* Hover effect - book moves up slightly */
#     .book-container:hover {
#         transform: translateY(-10px);
#         }
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
#      /* Sliding animation - books move left and right */
#         @keyframes sliding {
#             0% { transform: translateX(0); }
#             100% { transform: translateX(20px); }
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# header_col1, header_col2 = st.columns([1, 3])
# with header_col1:
#     st.image("assets/MalawiLibraryLogo.jpg", width= 100)  
#     st.markdown('<div class="header-title">📖 Malawi Library</div>', unsafe_allow_html=True)
# with header_col2:
#     search_col, login_col, signup_col = st.columns([3, 1, 1])
#     with search_col:
#         query = st.text_input("Search Books")
#         search_button = st.button("Search")
        
# st.markdown('<div class="butt-container">', unsafe_allow_html=True)
# with login_col:
#     if st.button("Log In"):
#         switch_page('login')

# with signup_col :
#     if st.button("Sign Up"):
#         switch_page('signup')
# st.markdown('</div>', unsafe_allow_html=True)   


# st.markdown(
#     """
#     <style>
#         .search-container {
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             gap: 10px;
#             margin-bottom: 20px;
#         }

#         .stTextInput>div>div>input {
#             padding: 10px;
#             font-size: 16px;
#             border: 2px solid #f1c40f;
#             border-radius: 8px;
#             width: 6000px;
#             background-color: #2c3e50;
#             color: white;
#         }

#         .stButton>button {
#             background-color: #f1c40f;
#             color: black;
#             font-size: 16px;
#             padding: 8px 16px;
#             border-radius: 8px;
#             border: none;
#             cursor: pointer;
#             transition: 0.3s;
#         }

#         .stButton>button:hover {
#             background-color: #e67e22;
#             color: white;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )  

# genres = fetch_genres()
# books = fetch_books()

# if search_button and query:
#     books = search_books(query)

# default_cover_url = "assets/coverpage.jpg" 

# for genre_id, genre_name in genres:
    
#     st.markdown(f"<h2>{genre_name}</h2><hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)
#     genre_books = [book for book in books if book[4] == genre_id]
    
#     book_cols = st.columns(3)  
#     for index, book in enumerate(genre_books[:3]): 
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
#                     </div>
#                     <div>
#                         <strong>{title}</strong><br>
#                         by {author}
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
#             with st.expander("Show Description"):
#                      summary = description[:200] + "..." if len(description) > 200 else description
#                      st.write(summary)
#             st.button("Borrow", key=f"{genre_id}_{book_id}_{index}")
   

# st.markdown(
#     """
#     <style>
#         .footer-container {
#             background-color: #2c3e50; /* Dark background for contrast */
#             color: white; /* White text for readability */
#             padding: 20px;
#             border-radius: 10px;
#             margin-top: 50px;
#             text-align: center;
#         }

#         .footer-container h3 {
#             color: #f1c40f; /* Highlighted text color */
#             margin-bottom: 10px;
#         }

#         .footer-columns {
#             display: flex;
#             justify-content: space-between;
#             gap: 40px;
#             padding: 10px 50px;
#         }

#         .footer-section {
#             flex: 1;
#             min-width: 200px;
#         }

#         .footer-container a {
#             color: #f1c40f;
#             text-decoration: none;
#             font-weight: bold;
#         }

#         .footer-container a:hover {
#             color: #e67e22; /* Different color on hover */
#         }

#         hr {
#             border: none;
#             height: 2px;
#             background: #f1c40f;
#             margin: 20px 0;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# st.markdown('<div class="footer-container">', unsafe_allow_html=True)

# with st.container():
#     st.markdown('<div class="footer-columns">', unsafe_allow_html=True)

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.markdown('<div class="footer-section">', unsafe_allow_html=True)
#         st.subheader("📌 About Us")
#         st.write("Malawi Library is an innovative book booking system where users can explore, reserve, and manage books with ease.")
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col2:
#         st.markdown('<div class="footer-section">', unsafe_allow_html=True)
#         st.subheader("📞 Contact Us")
#         st.write("✉️ Email: [contact@malawilibrary.com](mailto:contact@malawilibrary.com)")
#         st.write("📞 Phone: +123 456 7890")
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col3:
#         st.markdown('<div class="footer-section">', unsafe_allow_html=True)
#         st.subheader("📍 Location")
#         st.write("🏢 123 Library Street, Johannesburg, South Africa")
#         st.markdown('</div>', unsafe_allow_html=True)


# st.markdown('</div>', unsafe_allow_html=True)