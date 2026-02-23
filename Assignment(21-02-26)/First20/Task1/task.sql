CREATE DATABASE student_db;

USE student_db;

CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    course VARCHAR(100) NOT NULL
);

INSERT INTO students (name, age, course) VALUES
('John Doe', 20, 'Computer Science'),
('Jane Smith', 22, 'Mathematics'),
('Michael Brown', 19, 'Physics');