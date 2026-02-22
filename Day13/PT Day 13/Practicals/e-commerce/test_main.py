from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_item_201():
    res = client.post("/items", json={
        "title": "Phone",
        "description": "Android",
        "price": 20000,
        "stock": 10
    })
    assert res.status_code == 201
    assert res.json()["title"] == "Phone"

def test_get_items_200():
    res = client.get("/items")
    assert res.status_code == 200

def test_update_item_changes_data():
    created = client.post("/items", json={
        "title": "TV",
        "price": 30000,
        "stock": 3
    }).json()
    item_id = created["id"]

    res = client.put(f"/items/{item_id}", json={"price": 28000})
    assert res.status_code == 200
    assert res.json()["price"] == 28000

def test_delete_removes_task():
    created = client.post("/items", json={
        "title": "Mouse",
        "price": 500,
        "stock": 5
    }).json()
    item_id = created["id"]

    res = client.delete(f"/items/{item_id}")
    assert res.status_code == 200

    res2 = client.put(f"/items/{item_id}", json={"price": 100})
    assert res2.status_code == 404

def test_create_item_without_title_400_or_422():
    res = client.post("/items", json={
        "description": "No title",
        "price": 100,
        "stock": 1
    })
    # FastAPI validation error = 422
    assert res.status_code in (400, 422)

def test_get_non_existing_item_404_via_update():
    res = client.put("/items/999999", json={"price": 100})
    assert res.status_code == 404
