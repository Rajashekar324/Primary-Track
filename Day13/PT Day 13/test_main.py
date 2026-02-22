import pytest
from fastapi.testclient import TestClient

# Import models and factory function from main
from main import TaskBase, TaskCreate, TaskUpdate, Task, create_app


@pytest.fixture
def client():
    """Create a TestClient with a fresh app instance for each test."""
    app = create_app()
    return TestClient(app)


# ---------- GET /api/tasks Tests ----------
def test_get_all_tasks_empty(client):
    """Test getting all tasks when the list is empty."""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_tasks_with_data(client):
    """Test getting all tasks when tasks exist."""
    # Create a task first
    client.post("/api/tasks", json={"title": "Test Task", "description": "A test task"})
    
    # Get all tasks
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == "Test Task"


def test_get_single_task(client):
    """Test getting a single task by ID."""
    # Create a task
    create_response = client.post("/api/tasks", json={"title": "Single Task"})
    task_id = create_response.json()["id"]
    
    # Get that task
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Single Task"


def test_get_single_task_not_found(client):
    """Test getting a non-existent task returns 404."""
    response = client.get("/api/tasks/9999")
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]


# ---------- POST /api/tasks Tests ----------
def test_create_task(client):
    """Test creating a new task."""
    response = client.post(
        "/api/tasks",
        json={"title": "New Task", "description": "New Description", "completed": False}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Task"
    assert data["description"] == "New Description"
    assert data["completed"] is False
    assert "id" in data


def test_create_task_without_description(client):
    """Test creating a task without optional description."""
    response = client.post("/api/tasks", json={"title": "Task without description"})
    assert response.status_code == 201
    assert response.json()["title"] == "Task without description"


def test_create_task_with_custom_id(client):
    """Test creating a task with a custom ID."""
    response = client.post("/api/tasks", json={"title": "Custom ID Task", "id": 100})
    assert response.status_code == 201
    assert response.json()["id"] == 100


def test_create_task_duplicate_id(client):
    """Test that creating a task with a duplicate ID returns 409."""
    # Create first task with custom ID
    client.post("/api/tasks", json={"title": "Task 1", "id": 200})
    
    # Try to create another task with same ID
    response = client.post("/api/tasks", json={"title": "Task 2", "id": 200})
    assert response.status_code == 409
    assert "Task ID already exists" in response.json()["detail"]


def test_create_task_missing_title(client):
    """Test that missing title returns 400."""
    response = client.post("/api/tasks", json={"description": "No title"})
    assert response.status_code == 400


def test_create_task_empty_title(client):
    """Test that empty title returns 400."""
    response = client.post("/api/tasks", json={"title": ""})
    assert response.status_code == 400


# ---------- PUT /api/tasks Tests ----------
def test_update_task(client):
    """Test updating a task."""
    # Create a task
    create_response = client.post("/api/tasks", json={"title": "Original", "completed": False})
    task_id = create_response.json()["id"]
    
    # Update the task
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated", "completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["completed"] is True


def test_update_task_partial(client):
    """Test updating only some fields of a task."""
    # Create a task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Original", "description": "Original Description", "completed": False}
    )
    task_id = create_response.json()["id"]
    
    # Update only title
    response = client.put(f"/api/tasks/{task_id}", json={"title": "New Title"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["description"] == "Original Description"  # Should remain unchanged


def test_update_task_not_found(client):
    """Test updating a non-existent task returns 404."""
    response = client.put("/api/tasks/9999", json={"title": "Updated"})
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]


# ---------- DELETE /api/tasks Tests ----------
def test_delete_task(client):
    """Test deleting a task."""
    # Create a task
    create_response = client.post("/api/tasks", json={"title": "Task to Delete"})
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    """Test deleting a non-existent task returns 404."""
    response = client.delete("/api/tasks/9999")
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]
