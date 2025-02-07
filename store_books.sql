
-- CREATE TABLE userz(
--     user_id SERIAL PRIMARY KEY,
--     username VARCHAR(50) UNIQUE NOT NULL,
--     password VARCHAR(255) NOT NULL,
--     email VARCHAR(100) UNIQUE NOT NULL
-- );


-- CREATE TABLE categories (
--     category_id SERIAL PRIMARY KEY,
--     category_name VARCHAR(100) UNIQUE NOT NULL
-- );


-- CREATE TABLE authors (
--     author_id SERIAL PRIMARY KEY,
--     authors_name VARCHAR(255) UNIQUE NOT NULL
-- );
-- ALTER TABLE authors
-- RENAME COLUMN authors_name TO author_name

-- CREATE TABLE books (
--      id SERIAL PRIMARY KEY,
--      book_id VARCHAR , 
--      user_id int,
--      category_id INT,
--      title VARCHAR(255) NOT NULL,
--      author_id INT,
--      availability BOOLEAN DEFAULT TRUE,
--      published_date TEXT,
--      description VARCHAR,
--      FOREIGN KEY (user_id) REFERENCES userz(user_id),
--      FOREIGN KEY (category_id) REFERENCES categories(category_id),
--      FOREIGN KEY (author_id) REFERENCES authors(author_id)
-- );

ALTER TABLE books
ADD COLUMN cover_url VARCHAR(255);

-- CREATE TABLE bookings (
--     booking_id SERIAL PRIMARY KEY,
--     id integer,
--     user_id INT,
--     author_id INT,
--     booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     return_date DATE,
--     FOREIGN KEY(id) REFERENCES books(id),
--     FOREIGN KEY(user_id) REFERENCES userz(user_id),
--     FOREIGN KEY(author_id) REFERENCES authors(author_id)
-- );
-- ALTER TABLE bookings
-- ADD COLUMN  status VARCHAR(50) DEFAULT 'Pending'

--  ALTER TABLE bookings
-- ADD COLUMN collection_date DATE NOT NULL;

-- ALTER TABLE books  
-- ADD COLUMN book_id VARCHAR UNIQUE;

-- ALTER TABLE userz
-- RENAME COLUMN users_id TO user_id;
-- ALTER TABLE books
-- RENAME COLUMN users_id TO user_id


