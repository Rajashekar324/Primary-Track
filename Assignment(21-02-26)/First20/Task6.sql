-- -------------------------------------
-- 1. Create Database
-- -------------------------------------
CREATE DATABASE IF NOT EXISTS company_db;
USE company_db;

-- -------------------------------------
-- 2. Create Employees Table
-- -------------------------------------
CREATE TABLE IF NOT EXISTS employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    salary DECIMAL(10,2)
);

-- -------------------------------------
-- 3. Insert Sample Data
-- -------------------------------------
INSERT INTO employees (name, department, email, salary) VALUES
('John Smith', 'IT', 'john@company.com', 60000),
('Sara Khan', 'HR', 'sara@company.com', 50000),
('David Lee', 'IT', 'david@company.com', 70000),
('Emily Clark', 'Finance', 'emily@company.com', 65000),
('Michael Brown', 'HR', 'michael@company.com', 52000);

-- -------------------------------------
-- 4. View All Employees
-- -------------------------------------
SELECT * FROM employees;

-- -------------------------------------
-- 5. View Specific Columns
-- -------------------------------------
SELECT name, department, email, salary
FROM employees;

-- -------------------------------------
-- 6. Filter by Department (Example: IT)
-- -------------------------------------
SELECT *
FROM employees
WHERE department = 'IT';

-- -------------------------------------
-- 7. Get Unique Departments (Dropdown)
-- -------------------------------------
SELECT DISTINCT department
FROM employees;

-- -------------------------------------
-- 8. Optional: Sort by Salary (Highest First)
-- -------------------------------------
SELECT *
FROM employees
ORDER BY salary DESC;

-- -------------------------------------
-- 9. Optional: Limit Results (Pagination Example)
-- -------------------------------------
SELECT *
FROM employees
LIMIT 5 OFFSET 0;