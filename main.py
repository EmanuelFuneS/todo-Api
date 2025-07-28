from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world!"}

@app.get("/test")
async def test():
    return {"status": "API Ready!"}