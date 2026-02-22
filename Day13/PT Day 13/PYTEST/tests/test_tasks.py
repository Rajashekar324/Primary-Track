import pytest
from app import app, tasks

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        tasks.clear()
        yield client

def test_create_task(client):
    response = client.post("/api/tasks", json={"title": "Test Task"})
    assert response.status_code == 201

def test_get_all_tasks(client):
    client.post("/api/tasks", json={"title": "Task 1"})
    response = client.get("/api/tasks")
    assert response.status_code == 200

def test_update_task(client):
    res = client.post("/api/tasks", json={"title": "Old"})
    task_id = res.get_json()["id"]

    client.put(f"/api/tasks/{task_id}", json={"title": "New"})
    updated = client.get(f"/api/tasks/{task_id}")

    assert updated.get_json()["title"] == "New"

def test_delete_task(client):
    res = client.post("/api/tasks", json={"title": "Delete me"})
    task_id = res.get_json()["id"]

    client.delete(f"/api/tasks/{task_id}")
    response = client.get(f"/api/tasks/{task_id}")

    assert response.status_code == 404

def test_create_without_title(client):
    response = client.post("/api/tasks", json={"description": "No title"})
    assert response.status_code == 400

def test_get_non_existing_task(client):
    response = client.get("/api/tasks/999")
    assert response.status_code == 404

def test_update_non_existing_task(client):
    response = client.put("/api/tasks/999", json={"title": "Nothing"})
    assert response.status_code == 404

def test_invalid_json(client):
    response = client.post("/api/tasks", data="Not JSON")
    assert response.status_code == 400

def test_wrong_data_type(client):
    response = client.post("/api/tasks", json={
        "title": "Wrong type",
        "completed": "yes"
    })
    assert response.status_code == 400
