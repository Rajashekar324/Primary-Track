import os

# Task 1, 7, 10 → add function
def add(a, b):
    return a + b

# Task 2, 7 → subtract function
def subtract(a, b):
    return a - b

# Task 7 → multiply function
def multiply(a, b):
    return a * b

# Task 3 → string uppercase
def to_upper(text):
    return text.upper()

# Task 4 → list length
def list_length(lst):
    return len(lst)

# Task 5 → even number check
def is_even(num):
    return num % 2 == 0

# Task 6, 11 → division
def divide(a, b):
    return a / b

# Task 9 → square function
def square(x):
    return x * x

# Task 15 → mock API status
def get_status():
    return 200

# Task 18 → dictionary function
def get_user():
    return {"name": "Ravi", "age": 20}

# Task 12 → class for testing
class Calculator:
    def add(self, a, b):
        return a + b

# Task 16 → file exists
def file_exists(path):
    return os.path.exists(path)