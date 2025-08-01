from typing import List, Optional
from fastapi import HTTPException, status
from ..repositories.todo_repo import TodoRepository
from ..models.todo import TodoModel, UpdateTodoModel

class TodoService:
    def __init__(self, db=None):
        self.repository = TodoRepository(db)
    
    async def create_todo(self, todo: TodoModel) -> TodoModel:
        try:
            return await self.repository.create(todo)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating todo: {str(e)}"
            )
    
    async def get_all_todos(self, completed: Optional[bool] = None) -> List[TodoModel]:
        try:
            if completed is not None:
                return await self.repository.get_by_status(completed)
            return await self.repository.get_all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching todos: {str(e)}"
            )
    
    async def get_todo_by_id(self, todo_id: str) -> TodoModel:
        try:
            todo = await self.repository.get_by_id(todo_id)
            if not todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Todo {todo_id} not found"
                )
            return todo
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching todo: {str(e)}"
            )
    
    async def update_todo(self, todo_id: str, todo_update: UpdateTodoModel) -> TodoModel:
        try:
            updated_todo = await self.repository.update(todo_id, todo_update)
            if not updated_todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Todo {todo_id} not found"
                )
            return updated_todo
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating todo: {str(e)}"
            )
    
    async def delete_todo(self, todo_id: str) -> None:
        try:
            deleted = await self.repository.delete(todo_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Todo {todo_id} not found"
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting todo: {str(e)}"
            )