from typing import List, Optional
from bson import ObjectId
from pymongo import ReturnDocument
from ..core.database import get_database
from ..models.todo import TodoModel, UpdateTodoModel


class TodoRepository:
    def __init__(self, db=None):
        self.db = db or get_database()
        self.collection = self.db.todos
    
    async def create(self, todo: TodoModel) -> TodoModel:
        todo_dict = todo.model_dump(by_alias=True, exclude=["id"])
        result = await self.collection.insert_one(todo_dict)
        todo_dict["_id"] = result.inserted_id
        return TodoModel(**todo_dict)

    async def get_all(self, limit: int = 100) -> TodoModel:
        cursor = self.collection.find().limit(limit)
        todos= await cursor.to_list(length=limit)
        return [TodoModel(**todo) for todo in todos]
    
    async def get_by_id(self, todo_id: str) -> Optional[TodoModel]:
        todo = await self.collection.find_one({"_id": ObjectId(todo_id)})
        return TodoModel(**todo) if todo else None
    
    async def update(self, todo_id: str, todo_update: UpdateTodoModel) -> Optional[TodoModel]:
        update_data = {k: v for k, v in todo_update.model_dump().items() if v is not None}
        
        if not update_data:
            return await self.get_by_id(todo_id)
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(todo_id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        return TodoModel(**result) if result else None
    
    async def delete(self, todo_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(todo_id)})
        return result.deleted_count == 1
    
    async def get_by_status(self, completed: bool) -> List[TodoModel]:
        cursor = self.collection.find({"completed": completed})
        todos = await cursor.to_list(length=100)
        return [TodoModel(**todo) for todo in todos]