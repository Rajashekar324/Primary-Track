-- -----------------------------------
-- 1. Create Database
-- -----------------------------------
CREATE DATABASE IF NOT EXISTS quotes_db;
USE quotes_db;

-- -----------------------------------
-- 2. Create Quotes Table
-- -----------------------------------
CREATE TABLE IF NOT EXISTS quotes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    quote_text TEXT NOT NULL,
    author VARCHAR(100) NOT NULL
);

-- -----------------------------------
-- 3. Insert Sample Quotes
-- -----------------------------------
INSERT INTO quotes (quote_text, author) VALUES
('The only limit to our realization of tomorrow is our doubts of today.', 'Franklin D. Roosevelt'),
('Do what you can, with what you have, where you are.', 'Theodore Roosevelt'),
('Success is not final, failure is not fatal: it is the courage to continue that counts.', 'Winston Churchill'),
('In the middle of every difficulty lies opportunity.', 'Albert Einstein'),
('Believe you can and you''re halfway there.', 'Theodore Roosevelt');

-- -----------------------------------
-- 4. Display Random Quote (Main)
-- -----------------------------------
SELECT quote_text, author
FROM quotes
ORDER BY RAND()
LIMIT 1;

-- -----------------------------------
-- 5. Alternative Random Method (Optional for Large Tables)
-- -----------------------------------
SELECT *
FROM quotes
WHERE id = (
    SELECT FLOOR(1 + (RAND() * (SELECT MAX(id) FROM quotes)))
)
LIMIT 1;