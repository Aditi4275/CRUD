import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_full_crud():
    # Create
    r = client.post("/api/items/", json={"name": "Table", "description": "For working"})
    assert r.status_code == 200
    item_id = r.json()["id"]
    # Read
    r = client.get("/api/items/")
    assert any(i["id"] == item_id for i in r.json())
    # Update
    r = client.post(f"/items/{item_id}/edit", data={"name": "Table2", "description": "Updated"})
    assert r.status_code in (200, 303)
    # Delete
    r = client.post(f"/items/{item_id}/delete")
    assert r.status_code in (200, 303)
