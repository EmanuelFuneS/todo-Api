import os
import pymongo
from pymongo import AsyncMongoClient
from pymongo import ReturnDocument
from pymongo.server_api import ServerApi
from config import settings

class Database:
    client: AsyncMongoClient = None
    database = None
    
db= Database()

async def connect_to_mongo():
    
    db.client=AsyncMongoClient(os.environ["MONGODB_URL"], server_api=pymongo.server_api.ServiceApi(version="1", strict=True, deprecation_errors=True))

    db.database = db.client[settings.database_name]

async def close_mongo_connection():
    if db.client:
        db.client.close()
        
def get_database():
    return db.database