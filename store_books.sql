CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    availability BOOLEAN DEFAULT TRUE,
    published_date TEXT,
    category_id INT REFERENCES categories(category_id),
    author_id INT REFERENCES authors(author_id)
);

CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    book_id INT REFERENCES books(book_id),
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP
);


