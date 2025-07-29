from fastapi import FastAPI
from contextlib import asynccontextmanager
from .app.core.database import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(title="Todo API",description="A simple Toto Application API build with FastAPi and MongoDB",version="1.0.0",lifespan=lifespan)

app.include_router()

@app.get("/")
async def root():
    return {"message": "hello world!"}

@app.get("/test")
async def test():
    return {"status": "API Ready!"}
