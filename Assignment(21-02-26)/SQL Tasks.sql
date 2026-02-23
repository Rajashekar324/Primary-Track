-- =====================================================
-- TASK 1: Create Student Table and Insert Data
-- =====================================================

CREATE TABLE students (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50),
  age INT,
  course VARCHAR(50)
);

INSERT INTO students (name, age, course) VALUES
('Ravi', 19, 'Java'),
('Anjali', 22, 'Python'),
('Kiran', 21, 'C++'),
('Meena', 20, 'Java'),
('Arjun', 23, 'Python');


-- =====================================================
-- TASK 2: Retrieve All Records
-- =====================================================

SELECT * FROM students;


-- =====================================================
-- TASK 3: Retrieve Specific Columns
-- =====================================================

SELECT name, course FROM students;


-- =====================================================
-- TASK 4: Use WHERE Condition
-- =====================================================

SELECT * FROM students WHERE age > 20;


-- =====================================================
-- TASK 5: Use ORDER BY (Ascending and Descending)
-- =====================================================

-- Ascending
SELECT * FROM students ORDER BY age ASC;

-- Descending
SELECT * FROM students ORDER BY age DESC;


-- =====================================================
-- TASK 6: Use LIMIT
-- =====================================================

SELECT * FROM students LIMIT 3;


-- =====================================================
-- TASK 7: Update Records
-- =====================================================

UPDATE students SET course = 'Python' WHERE id = 1;


-- =====================================================
-- TASK 8: Delete Record
-- =====================================================

DELETE FROM students WHERE id = 3;


-- =====================================================
-- TASK 9: Use DISTINCT
-- =====================================================

SELECT DISTINCT course FROM students;


-- =====================================================
-- TASK 10: Use COUNT Function
-- =====================================================

SELECT COUNT(*) AS total_students FROM students;


-- =====================================================
-- TASK 11: Use MAX and MIN
-- =====================================================

SELECT 
  MAX(age) AS oldest_student,
  MIN(age) AS youngest_student
FROM students;


-- =====================================================
-- TASK 12: Use AVG Function
-- =====================================================

SELECT AVG(age) AS average_age FROM students;


-- =====================================================
-- TASK 13: Use GROUP BY
-- =====================================================

SELECT course, COUNT(*) AS student_count
FROM students
GROUP BY course;


-- =====================================================
-- TASK 14: Use HAVING
-- =====================================================

SELECT course, COUNT(*) AS student_count
FROM students
GROUP BY course
HAVING COUNT(*) > 1;


-- =====================================================
-- TASK 15: Create Courses Table (Relationship)
-- =====================================================

CREATE TABLE courses (
  id INT PRIMARY KEY AUTO_INCREMENT,
  course_name VARCHAR(50)
);

INSERT INTO courses (course_name) VALUES
('Java'),
('Python'),
('C++');

-- Add course_id column to students for joining
ALTER TABLE students ADD course_id INT;

-- Update course_id values manually (example mapping)
UPDATE students SET course_id = 1 WHERE course = 'Java';
UPDATE students SET course_id = 2 WHERE course = 'Python';
UPDATE students SET course_id = 3 WHERE course = 'C++';


-- =====================================================
-- TASK 16: INNER JOIN
-- =====================================================

SELECT students.name, courses.course_name
FROM students
INNER JOIN courses
ON students.course_id = courses.id;


-- =====================================================
-- TASK 17: LEFT JOIN
-- =====================================================

SELECT students.name, courses.course_name
FROM students
LEFT JOIN courses
ON students.course_id = courses.id;


-- =====================================================
-- TASK 18: Use Subquery
-- =====================================================

SELECT name
FROM students
WHERE age > (SELECT AVG(age) FROM students);


-- =====================================================
-- TASK 19: Create View
-- =====================================================

CREATE VIEW student_view AS
SELECT name, course FROM students;


-- =====================================================
-- TASK 20: Create Index
-- =====================================================

CREATE INDEX idx_name ON students(name);