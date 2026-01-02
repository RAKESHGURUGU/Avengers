from fastapi import FastAPI

app = FastAPI( title="Avengers API", version="1.0.0" )
@app.get("/")
async def read_root():
    return {"Hello": "World"}
