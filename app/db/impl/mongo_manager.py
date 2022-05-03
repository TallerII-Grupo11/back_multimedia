import logging
from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.db import DatabaseManager
from app.db.models import SongModel, PyObjectId, UpdateSongModel
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


    async def get_songs(self) -> List[UpdateSongModel]:
        songs_list = []
        songs_q = self.db["songs"].find()
        async for song in songs_q:
            songs_list.append(SongModel(**song))
        return songs_list


    async def get_song(self, song_id: str) -> SongModel:
        song = await self.db["songs"].find_one({"_id": song_id})
        return song

    async def delete_song(self, song_id: str):
        delete_result = await self.db["songs"].delete_one({"_id": song_id})
        return delete_result
        #await self.db.posts.delete_one({'_id': ObjectId(post_id)})

    async def update_song(self, song_id: str, song: UpdateSongModel):
        song = {k: v for k, v in song.dict().items() if v is not None}

        if len(song) >= 1:
            update_result = await self.db["songs"].update_one({"_id": song_id}, {"$set": song})

            if update_result.modified_count == 1:
                return update_result
            else:
                return None

    async def add_song(self, song: SongModel):
        #song = SongModel.parse_obj(song) #song.dict()#jsonable_encoder(song)
        new_song = await self.db["songs"].insert_one(song)
        return new_song
        #await self.db.posts.insert_one(post.dict(exclude={'id'}))