import pytest
from app import Calculator, file_exists

# Task 14 → setup_method usage
class TestCalculator:

    def setup_method(self):
        self.calc = Calculator()

    # Task 12 → class method test
    def test_add(self):
        assert self.calc.add(2, 3) == 5

# Task 16 → file exists test
def test_file_exists(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")
    assert file_exists(file)