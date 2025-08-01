import pytest
from app.services.todo_service import TodoService
from app.repositories.todo_repo import TodoRepository
from app.models.todo import TodoModel


@pytest.mark.asyncio
async def test_service_create_todo(test_db, sample_todo_dict):
    repo = TodoRepository(test_db)
    service = TodoService(repo)
    
    todo_model = TodoModel(**sample_todo_dict)
    result = await service.create_todo(todo_model)
    
    assert isinstance(result, TodoModel)
    assert result.title == sample_todo_dict["title"]
    assert result.id is not None


@pytest.mark.asyncio
async def test_service_get_all_todos(test_db, sample_todo_dict):
    repo = TodoRepository(test_db)
    service = TodoService(repo)
    
    todo_model = TodoModel(**sample_todo_dict)
    await service.create_todo(todo_model)
    todos = await service.get_all_todos()
    
    assert isinstance(todos, list)
    assert all(isinstance(todo, TodoModel) for todo in todos)