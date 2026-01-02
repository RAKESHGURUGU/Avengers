from fastapi import FastAPI
from .database import engine
from . import models
from .routers import programs, branches, courses, faculties

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WEBSAGA API", version="1.0.0")

app.include_router(programs.router)
app.include_router(branches.router)
app.include_router(courses.router)
app.include_router(faculties.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to WEBSAGA API"}
