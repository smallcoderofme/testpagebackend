from fastapi import FastAPI
import pydantic
from sqlalchemy import create_engine
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
import uuid
from sqlalchemy.sql import select

DATABASE_URI = 'postgresql://sunshuai:123456@localhost/tempDB'
DATABASE_MIN_POOL_SIZE = 10
DATABASE_MAX_POOL_SIZE = 50
database = Database(DATABASE_URI)

from .controller.post import post_router
from .controller.user import user_router
from .models.model import metadata

engine = create_engine(
    DATABASE_URI
)
metadata.create_all(engine)

def create_app():
    app = FastAPI()

    origins = [
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        expose_headers=["x-xsrf-token"],
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(post_router)
    app.include_router(user_router)

    return app

app = create_app()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}