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
        book_id = book['id']
        title = book['volumeInfo'].get('title', 'No title')
        published_date = book['volumeInfo'].get('publishedDate', 'Unknown')
        genres = book['volumeInfo'].get('categories', [])
        description = book['volumeInfo'].get('description', 'No description available')  # Now used for categories
        authors = book['volumeInfo'].get('authors', [])

        # Store categories with descriptions
        category_ids = []
        for genre in genres:
            cur.execute(
                """
                INSERT INTO categories (genre_name, description) 
                VALUES (%s, %s) 
                ON CONFLICT (genre_name) DO NOTHING RETURNING category_id
                """,
                (genre, description)
            )
            category_id = cur.fetchone()
            if not category_id:
                cur.execute("SELECT category_id FROM categories WHERE genre_name = %s", (genre,))
                category_id = cur.fetchone()

            if category_id:
                category_ids.append(category_id[0])

        # Store authors
        author_ids = []
        for author in authors:
            cur.execute(
                "INSERT INTO authors (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING authors_id",
                (author,))
            authors_id = cur.fetchone()
            if not authors_id:
                cur.execute("SELECT authors_id FROM authors WHERE name = %s", (author,))
                authors_id = cur.fetchone()

            if authors_id:
                author_ids.append(authors_id[0])

        # Insert book with the first category and author (adjust logic if needed)
        category_id = category_ids[0] if category_ids else None
        authors_id = author_ids[0] if author_ids else None

        if category_id and authors_id:  # Ensure valid IDs before inserting
            cur.execute(
                "INSERT INTO books (book_id, title, availability, published_date, category_id, authors_id) "
                "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (book_id) DO NOTHING",
                (book_id, title, True, published_date, category_id, authors_id)
            )

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    api_key = "AIzaSyANI3YMtiYA_9fa0lmlaXzaSFLrQA1R9Sk"  # Replace with your actual API key
    query = "Python programming"  # Replace with your desired search query
    books = fetch_books_from_google(query, api_key)
    store_books(books)


