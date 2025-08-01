import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_todo_endpoint(async_client: AsyncClient, sample_todo_dict):
    
    response = await async_client.post("/api/v1/todos/", json=sample_todo_dict)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_todo_dict["title"]
    assert data["description"] == sample_todo_dict["description"]
    assert "id" in data

@pytest.mark.asyncio
async def test_get_todos_endpoint(async_client: AsyncClient):
    response = await async_client.get("/api/v1/todos/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
@pytest.mark.asyncio
async def test_get_todo_by_id_endpoint(async_client: AsyncClient, sample_todo_dict):
    create_response = await async_client.post("/api/v1/todos/", json=sample_todo_dict)
    create_todo= create_response.json()
    
    response = await async_client.get(f"/api/v1/todos/{create_todo['id']}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == create_todo["id"]
    assert data["description"] == create_todo["description"]
    
@pytest.mark.asyncio
async def test_update_todo_endpoint(async_client: AsyncClient, sample_todo_dict):
    create_response = await async_client.post("/api/v1/todos/", json=sample_todo_dict)
    created_todo = create_response.json()
    
    update_data = {"title": "Updated via API", "completed": True}
    response = await async_client.put(f"/api/v1/todos/{created_todo['id']}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated via API"
    assert data["completed"] == True


@pytest.mark.asyncio
async def test_delete_todo_endpoint(async_client: AsyncClient, sample_todo_dict):
    create_response = await async_client.post("/api/v1/todos/", json=sample_todo_dict)
    created_todo = create_response.json()

    response = await async_client.delete(f"/api/v1/todos/{created_todo['id']}")
    
    assert response.status_code == 204
    
    get_response = await async_client.get(f"/api/v1/todos/{created_todo['id']}")
    assert get_response.status_code == 404
    