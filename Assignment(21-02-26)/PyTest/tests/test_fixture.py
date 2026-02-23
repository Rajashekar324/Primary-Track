import pytest

# Task 8 → simple fixture
@pytest.fixture
def sample_data():
    return [1, 2, 3, 4]

def test_sample_data_length(sample_data):
    assert len(sample_data) == 4

# Task 13 → mock database fixture
@pytest.fixture
def mock_db():
    return {"id": 1, "name": "Test User"}

def test_mock_db(mock_db):
    assert mock_db["name"] == "Test User"

# Task 19 → fixture with module scope
@pytest.fixture(scope="module")
def module_data():
    return [10, 20, 30]

def test_module_data_1(module_data):
    assert sum(module_data) == 60

def test_module_data_2(module_data):
    assert len(module_data) == 3