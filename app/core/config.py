import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "todo_db"
    collection_name: str = "todos"
    
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        case_sensitive = False
        

settings = Settings()