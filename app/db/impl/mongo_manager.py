import logging
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.db import DatabaseManager
from app.db.model.song import SongModel, UpdateSongModel
from app.db.model.album import AlbumModel, UpdateAlbumModel, AlbumSongModel
from app.db.model.subscription import Subscription
from fastapi import Body
from fastapi.encoders import jsonable_encoder


class MongoManager(DatabaseManager):
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str):
        logging.info("Connecting to MongoDB.")
        self.client = AsyncIOMotorClient(
            path,
            maxPoolSize=10,
            minPoolSize=10)
        # Multimedia is main_db
        self.db = self.client.multimedia
        logging.info("Connected to MongoDB.")

    async def close_database_connection(self):
        logging.info("Closing connection with MongoDB.")
        self.client.close()
        logging.info("Closed connection with MongoDB.")