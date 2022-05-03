import uvicorn

import logging.config

from app.adapters.http.songs import songs_controller
from fastapi import FastAPI

from app.conf.config import Settings
from app.conf.mongodb import MongoDB

import os

from fastapi import Body
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status


logging.config.fileConfig('app/conf/logging.conf', disable_existing_loggers=False)

settings = Settings()

db = MongoDB()

app = FastAPI(
    version=settings.version, title=settings.title, description=settings.description
)

logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    logger.info("Startup APP")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutdown APP")


app.include_router(songs_controller.router)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=settings.port)
