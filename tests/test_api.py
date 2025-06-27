import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_update_and_delete_item():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create
        response = await ac.post("/api/items/", json={"name": "Table", "description": "For working"})
        assert response.status_code == 200
        item_id = response.json()["id"]

        # Update
        response = await ac.put(f"/api/items/{item_id}", json={"name": "Table2", "description": "Updated"})
        assert response.status_code in (200, 204)

        # Get single
        response = await ac.get(f"/api/items/{item_id}")
        assert response.status_code == 200

        # Delete
        response = await ac.delete(f"/api/items/{item_id}")
        assert response.status_code in (200, 204)

        # Get after delete
        response = await ac.get(f"/api/items/{item_id}")
        assert response.status_code == 404
