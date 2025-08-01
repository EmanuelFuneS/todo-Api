from typing import List, Optional
from fastapi import APIRouter, Body, status, Query
from fastapi.responses import Response
from ..models.todo import TodoModel, UpdateTodoModel
from ..services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post(
    "/",
    response_model=TodoModel,
    status_code=status.HTTP_201_CREATED,
    response_description="Create new todo"
)
async def create_todo(todo: TodoModel = Body(...)):
    todo_service = TodoService()
    return await todo_service.create_todo(todo)

@router.get(
    "/",
    response_model=List[TodoModel],
    response_description="List all todos"
)
async def list_todos(completed: Optional[bool] = Query(None, description="Filter by completion status")):
    todo_service = TodoService()
    return await todo_service.get_all_todos(completed)

@router.get(
    "/{todo_id}",
    response_model=TodoModel,
    response_description="Get todo by ID"
)
async def get_todo(todo_id: str):
    todo_service = TodoService()
    return await todo_service.get_todo_by_id(todo_id)

@router.put(
    "/{todo_id}",
    response_model=TodoModel,
    response_description="Update todo"
)
async def update_todo(todo_id: str, todo_update: UpdateTodoModel = Body(...)):
    todo_service = TodoService()
    return await todo_service.update_todo(todo_id, todo_update)

@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete todo"
)
async def delete_todo(todo_id: str):
    todo_service = TodoService()
    await todo_service.delete_todo(todo_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)