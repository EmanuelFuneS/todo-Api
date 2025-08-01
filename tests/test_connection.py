import asyncio
import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

@pytest.mark.asyncio
async def test_connection():
    client = AsyncIOMotorClient(settings.mongodb_url)
    try:
        await client.admin.command('ping')

        dbs= await client.list_database_names()
        print(f"Data Bases: {dbs}")
        assert isinstance(dbs, list)

    except Exception as e:
        print(f"Error Conn:{e}")
        pytest.fail(f"Connection failed: {e}")
    finally:
        client.close()