import logging

from contextlib import asynccontextmanager
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from db import database
from routers.posts import router as posts_router
from logging_conf import configure_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)
app.include_router(posts_router)


@app.exception_handler(HTTPException)
async def http_exception_logger(request, exc):
    logger.error(f"HTTP exception: {exc.status_code} | {exc.detail}")
    return await http_exception_handler(request, exc)
