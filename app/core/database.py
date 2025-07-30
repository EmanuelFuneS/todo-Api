import os
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from .config import settings

class Database:
    client: AsyncIOMotorClient = None
    database = None
    
db= Database()

async def connect_to_mongo():
    
    db.client=AsyncIOMotorClient(settings.mongodb_url, server_api=ServerApi(version="1", strict=True, deprecation_errors=True))

    db.database = db.client[settings.database_name]

async def close_mongo_connection():
    if db.client:
        db.client.close()
        
def get_database():
    return db.database