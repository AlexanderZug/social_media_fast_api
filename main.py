from contextlib import asynccontextmanager

from fastapi import FastAPI

from db import database
from routers.posts import router as posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(posts_router)
