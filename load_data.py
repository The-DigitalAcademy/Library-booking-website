import requests
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname="store_books",
        user="postgres",
        password="",
        host="localhost"
    )
    return conn

def fetch_books_from_google(query, api_key):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error: {response.status_code}")
        return []


def store_books(books):
    conn = get_db_connection()
    cur = conn.cursor()

    for book in books:
        title = book['volumeInfo'].get('title', 'No title')
        description = book['volumeInfo'].get('description', 'No description')
        published_date = book['volumeInfo'].get('publishedDate', 'Unknown')
        categories = book['volumeInfo'].get('categories', [])
        authors = book['volumeInfo'].get('authors', [])

        for category in categories:
            cur.execute("INSERT INTO categories (category_name) VALUES (%s) ON CONFLICT (category_name) DO NOTHING RETURNING category_id", (category,))
            category_id = cur.fetchone()
            if category_id:
                category_id = category_id[0]
            else:
                cur.execute("SELECT category_id FROM categories WHERE category_name = %s", (category,))
                category_id = cur.fetchone()[0]


        for author in authors:
            cur.execute("INSERT INTO authors (authors_name) VALUES (%s) ON CONFLICT (authors_name) DO NOTHING RETURNING author_id", (author,))
            author_id = cur.fetchone()
            if author_id:
                author_id = author_id[0]
            else:
                cur.execute("SELECT author_id FROM authors WHERE authors_name = %s", (author,))
                author_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO books (book_id, title, description, availability, published_date, category_id, author_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (book['id'], title, description, True, published_date, category_id, author_id)
        )

    conn.commit()
    cur.close()
    conn.close()

if __name__== "main":
    api_key = "AIzaSyANI3YMtiYA_9fa0lmlaXzaSFLrQA1R9Sk"
    query = "Python programming"
    books = fetch_books_from_google(query, api_key)
    store_books(books)
