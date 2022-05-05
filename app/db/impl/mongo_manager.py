import logging
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.db import DatabaseManager
from app.db.model.song import SongModel, UpdateSongModel
from app.db.model.album import AlbumModel, UpdateAlbumModel
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

    # --- SONG ---
    async def get_songs(self) -> List[UpdateSongModel]:
        songs_list = []
        songs_q = self.db["songs"].find()
        async for song in songs_q:
            songs_list.append(SongModel(**song))
        return songs_list

    async def get_song(self, song_id: str) -> SongModel:
        song = await self.db["songs"].find_one({"_id": song_id})
        return SongModel(**song)

    async def delete_song(self, song_id: str):
        delete_result = await self.db["songs"].delete_one({"_id": song_id})
        return delete_result

    async def update_song(self, song_id: str, song: UpdateSongModel = Body(...)):
        song = {k: v for k, v in song.dict().items() if v is not None}

        if len(song) >= 1:
            await self.db["songs"].update_one({"_id": song_id}, {"$set": song})

    async def add_song(self, song: SongModel = Body(...)):
        song = jsonable_encoder(song)
        await self.db["songs"].insert_one(song)
        return song

    # --- ALBUM ---
    async def get_albums(self) -> List[UpdateAlbumModel]:
        albums_list = []
        albums_q = self.db["albums"].find()
        async for album in albums_q:
            albums_list.append(AlbumModel(**album))
        return albums_list

    async def get_album(self, album_id: str) -> AlbumModel:
        album = await self.db["albums"].find_one({"_id": album_id})
        return album

    async def delete_album(self, album_id: str):
        delete_result = await self.db["albums"].delete_one({"_id": album_id})
        return delete_result

    async def update_album(self, album_id: str, album: UpdateAlbumModel = Body(...)):
        album = {k: v for k, v in album.dict().items() if v is not None}

        if len(album) >= 1:
            await self.db["albums"].update_one({"_id": album_id}, {"$set": album})

    async def add_album(self, album: AlbumModel = Body(...)):
        album = jsonable_encoder(album)
        await self.db["albums"].insert_one(album)
        return album
