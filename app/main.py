from fastapi import FastAPI

from .database import Base, engine
from .routers import projects, places

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Planner API")

app.include_router(projects.router)
app.include_router(places.router)


@app.get("/")
def root():
    return {"message": "Travel Planner API"}
