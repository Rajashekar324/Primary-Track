import pytest
from app import *

# Task 1 → test add function
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

# Task 2 → subtraction test
def test_subtract():
    assert subtract(5, 2) == 3
    assert subtract(0, 5) == -5

# Task 3 → uppercase string
def test_upper():
    assert to_upper("hello") == "HELLO"
    assert to_upper("python") == "PYTHON"

# Task 4 → list length
def test_list_length():
    assert list_length([1, 2, 3]) == 3
    assert list_length([]) == 0

# Task 5 → even number test
def test_is_even():
    assert is_even(4) is True
    assert is_even(5) is False

# Task 6 → division test
def test_divide():
    assert divide(10, 2) == 5

# Task 7 → multiple functions in one file
def test_multiple_functions():
    assert add(1, 2) == 3
    assert subtract(5, 2) == 3
    assert multiply(2, 3) == 6

# Task 9 → square multiple inputs
def test_square_multiple():
    assert square(2) == 4
    assert square(5) == 25
    assert square(0) == 0

# Task 10 → parametrize test
@pytest.mark.parametrize("a,b,result", [
    (1, 2, 3),
    (5, 5, 10),
    (-1, 1, 0)
])
def test_add_parametrize(a, b, result):
    assert add(a, b) == result

# Task 11 → exception handling
def test_divide_exception():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

# Task 15 → API mock response
def test_api_status():
    assert get_status() == 200

# Task 17 → list contains value
def test_list_contains():
    data = [1, 2, 3]
    assert 2 in data

# Task 18 → dictionary values
def test_dictionary_values():
    user = get_user()
    assert user["name"] == "Ravi"
    assert user["age"] == 20

# Task 20 → pytest marker
@pytest.mark.slow
def test_slow_operation():
    assert add(10, 10) == 20