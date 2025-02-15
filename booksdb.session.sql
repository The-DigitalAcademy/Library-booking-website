-- DELETE FROM books WHERE user_id = 1;
-- SELECT id, book_id, availability FROM books WHERE book_id = 'RQ6xDwAAQBAJ';  

-- DELETE FROM categories  
-- WHERE category_name = 'Romance';

-- WHERE category_name IN ('Stats', 'Mathematics', 'mathematics', 'maths',  'statistics', 'Animal', 'poet');
-- DELETE FROM categories
-- WHERE category_name IN ('Chemistry', 'Statistics')

-- UPDATE categories
-- SET category_name = 'Statistics Books'
-- WHERE category_name = 'Statistics';
-- DELETE FROM bookings WHERE id = 284;

-- ALTER TABLE userz
-- ADD COLUMN role VARCHAR(10) CHECK (role IN ('admin', 'user')) NOT NULL DEFAULT 'user';

DELETE FROM userz WHERE role = 'admin';

-- DELETE FROM bookings WHERE booking_id = 285;

-- ALTER TABLE userz
--  ADD COLUMN agreement_accepted BOOLEAN DEFAULT FALSE;