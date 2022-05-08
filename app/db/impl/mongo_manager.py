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

    async def list_songs_by_album(self, album_id: str = None) -> List[UpdateSongModel]:
        songs_list = []
        songs_q = self.db["songs"].find({"album_id": album_id})
        async for song in songs_q:
            songs_list.append(SongModel(**song))
        return songs_list

    # --- ALBUM ---
    async def with_songs(self, album: AlbumModel):
        songs_list = []
        for song_id in album["songs"]:
            song = await self.get_song(song_id)
            songs_list.append(song)

        album_w_song = {"songs": songs_list,
                        "artist": album["artist"],
                        "title": album["title"],
                        "description": album["description"],
                        "genre": album["genre"],
                        "subscription": album["subscription"],
                        "images": album["images"]
        }
        return AlbumSongModel.parse_obj(album_w_song)

    async def get_albums(self) -> List[UpdateAlbumModel]:
        albums_list = []
        albums_q = self.db["albums"].find()
        async for album in albums_q:
            albums_list.append(AlbumModel(**album))
        return albums_list

    async def get_album(self, album_id: str) -> AlbumSongModel:
        album = await self.db["albums"].find_one({"_id": album_id})
        album_w_song = await self.with_songs(album)

        return album_w_song

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

    async def get_albums_by_artist(self, artist: str) -> List[AlbumSongModel]:
        albums_list = []
        albums_q = self.db["albums"].find({"artist": artist})
        async for album in albums_q:
            alb = await self.with_songs(album)
            albums_list.append(alb)
        return albums_list

    async def get_albums_by_subscription(
        self, 
        subscription: str
    ) -> List[UpdateAlbumModel]:
        albums_list = []
        albums_q = self.db["albums"].find(
            {"subscription": 
                {"$in": Subscription.get_allowed(subscription)} 
            }
        )
        async for album in albums_q:
            albums_list.append(AlbumModel(**album))
        return albums_list