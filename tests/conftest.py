import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from app.main import app
from app.core.database import get_database
from app.core.config import settings
from app.repositories.todo_repo import TodoRepository
import os
import asyncio


test_database_name = "todo_db_test"

_test_client = None

async def get_test_client():
    global _test_client
    if _test_client is None:
        _test_client = AsyncIOMotorClient(settings.mongodb_url)
    return _test_client

@pytest_asyncio.fixture(scope="session")
async def mongodb_client():
    client = await get_test_client()
    yield client

@pytest_asyncio.fixture(scope="function")
async def test_db(mongodb_client):
    test_db = mongodb_client[test_database_name]
    yield test_db
    try:
        collections = await test_db.list_collection_names()
        for collection_name in collections:
            await test_db[collection_name].delete_many({})
    except Exception:
        pass

@pytest_asyncio.fixture(scope="function")
async def todo_repo(test_db):
    """Fixture que proporciona una instancia de TodoRepository con la base de datos de prueba"""
    return TodoRepository(db=test_db)

@pytest_asyncio.fixture(scope="function")
async def async_client(test_db):
    def get_test_database():
        return test_db
    app.dependency_overrides[get_database] = get_test_database
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_todo_dict():
    return {
        'title': 'test todo',
        'description': 'this is a test todo',
        'completed': False
    }

@pytest.fixture
def sample_todo_model(sample_todo_dict):
    from app.models.todo import TodoModel
    return TodoModel(**sample_todo_dict)

@pytest.fixture(scope="session")
def event_loop():
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()