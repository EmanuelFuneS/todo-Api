import os
from pydantic_settings import baseSettings

class Settings(baseSettings):
    mongodb_url= str
    database_name: str = "todo_db"
    collection_name: str = "todos"
    
    class Config:
        env_file=".env"
        
settings = Settings()