from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_item():
    # Create
    response = client.post("/api/items/", json={"name": "Chair", "description": "For sitting"})
    assert response.status_code == 200
    item = response.json()
    # Get
    response = client.get("/api/items/")
    assert response.status_code == 200
    items = response.json()
    assert any(i['name'] == "Chair" for i in items)
