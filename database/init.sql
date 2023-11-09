USE Library;

CREATE TABLE authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    publication_year INT,
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

INSERT INTO authors (first_name, last_name) VALUES
    ('J.K.', 'Rowling'),
    ('George R.R.', 'Martin'),
    ('J.R.R.', 'Tolkien');

INSERT INTO books (title, publication_year, author_id) VALUES
    ('Harry Potter and the Sorcerer''s Stone', 1997, 1),
    ('A Game of Thrones', 1996, 2),
    ('The Fellowship of the Ring', 1954, 3);