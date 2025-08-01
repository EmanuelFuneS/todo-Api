from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.database import connect_to_mongo, close_mongo_connection, db

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await connect_to_mongo()
    except Exception as e:
        print(f"❌ Error conn DB: {e}")
    
    yield
    
    await close_mongo_connection()

app = FastAPI(
    title="Todo API",
    description="A simple Todo Application API built with FastAPI and MongoDB",
    version="1.0.0",
    lifespan=lifespan
)


try:
    from .routers import todos
    app.include_router(todos.router, prefix="/api/v1")

except Exception as e:
    print(f"⚠️ Error loading routes: {e}")

@app.get("/")
async def root():
    return {
        "message": "¡TODO API Ready!", 
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "OK"
    }

@app.get("/health")
async def health_check():
    try:
        db_status = "connected" if db.database else "disconnected"
    except:
        db_status = "error"
    
    return {
        "status": "healthy", 
        "service": "TODO API",
        "database": db_status
    }