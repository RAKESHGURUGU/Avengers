from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import programs, branches, courses, faculties, auth, regulations, generated_qps

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WEBSAGA API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(programs.router)
app.include_router(branches.router)
app.include_router(courses.router)
app.include_router(faculties.router)
app.include_router(regulations.router)
app.include_router(auth.router)
app.include_router(generated_qps.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to WEBSAGA API"}
