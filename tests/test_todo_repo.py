import pytest
from app.repositories.todo_repo import TodoRepository
from app.models.todo import TodoModel


@pytest.mark.asyncio
async def test_create_todo(test_db, sample_todo_dict):
    todo_repository = TodoRepository(test_db)
    todo  = TodoModel(**sample_todo_dict)
    created_todo = await todo_repository.create(todo)
    
    assert created_todo.title == sample_todo_dict["title"]
    assert created_todo.description == sample_todo_dict["description"]
    assert created_todo.completed == sample_todo_dict["completed"]
    assert created_todo.id is not None

@pytest.mark.asyncio
async def test_get_all_todos(test_db, sample_todo_dict):
    todo_repository = TodoRepository(test_db)
    todo1 = TodoModel(**sample_todo_dict)
    todo2 = TodoModel(title="second todo", description="Another test", completed=True)
    
    await todo_repository.create(todo1)
    await todo_repository.create(todo2)
    
    todos = await todo_repository.get_all()
    
    assert len(todos) >= 2
    assert all(isinstance(todo, TodoModel) for todo in todos)
    
@pytest.mark.asyncio
async def test_get_todo_by_id(test_db, sample_todo_dict):
    todo_repository = TodoRepository(test_db)
    todo = TodoModel(**sample_todo_dict)
    create_todo = await todo_repository.create(todo)
    
    update_data = {"title": "update title", "completed": True}
    update_todo = await todo_repository.update(create_todo.id, update_data)
    
    assert update_todo.title == "update title"
    assert update_todo.completed == True
    assert update_todo.id == create_todo.id
    
@pytest.mark.asyncio
async def test_delete_todo(test_db, sample_todo_dict):
    todo_repository = TodoRepository(test_db)
    todo = TodoModel(**sample_todo_dict)
    create_todo = await todo_repository.create(todo)
    
    result = await todo_repository.delete(create_todo.id)
    assert result == True
    
    delete_todo = await todo_repository.get_by_id(create_todo.id)
    assert delete_todo is None
    
    