import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

@pytest.mark.asyncio
async def test_database_connection():
    client = AsyncIOMotorClient(settings.mongodb_url)
    try:
        result = await client.admin.command('ping')
        assert result.get('ok') ==1.0
        
        dbs = await client.list_database_names()
        print(f"Databases available: {dbs}")
        
        assert isinstance(dbs, list)
        assert len(dbs) > 0
        
    except Exception as e:
        pytest.fail(f"connection failed: {e}")
    finally:
        client.close()    