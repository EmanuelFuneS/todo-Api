from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class TodoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example":{
                "title": "example",
                "description": "example",
                "completed" : False,
                "priority": "medium"
            }
        }
    )
    
class UpdateTodoModel(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    
    model_config = ConfigDict(arbitrary_types_allowed=True)