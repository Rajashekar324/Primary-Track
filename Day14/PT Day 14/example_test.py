import pytest
from example import add, subtract, multiply, divide, calculate_grade


# ---------------- FIXTURE ----------------
@pytest.fixture
def sample_numbers():
    return 10, 5


def test_add_fixture(sample_numbers):
    a, b = sample_numbers
    assert add(a, b) == 15


# ---------------- PARAMETRIZE ----------------
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (5, 5, 10),
        (-1, 1, 0),
    ],
)
def test_add_parametrize(a, b, expected):
    assert add(a, b) == expected


# ---------------- EXCEPTION TESTING ----------------
def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)


# ---------------- BUSINESS LOGIC TESTING ----------------
@pytest.mark.parametrize(
    "marks, grade",
    [
        (95, "A"),
        (80, "B"),
        (60, "C"),
        (40, "Fail"),
    ],
)
def test_calculate_grade(marks, grade):
    assert calculate_grade(marks) == grade


def test_invalid_marks():
    with pytest.raises(ValueError):
        calculate_grade(150)