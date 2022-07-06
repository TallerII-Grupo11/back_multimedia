from typing import List
import logging

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.model.song import SongModel, UpdateSongModel
from fastapi import Body
from fastapi.encoders import jsonable_encoder


class SongManager:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_all_songs(self) -> List[SongModel]:
        songs_list = []
        songs_q = self.db["songs"].find()
        async for song in songs_q:
            songs_list.append(SongModel(**song))
        return songs_list

    async def get_song(self, song_id: str) -> UpdateSongModel:
        song = await self.db["songs"].find_one({"_id": song_id})
        logging.info(f"[SONG] {song}")
        return song

    async def delete_song(self, song_id: str):
        delete_result = await self.db["songs"].delete_one({"_id": song_id})
        return delete_result

    async def update_song(
        self, song_id: str, song: UpdateSongModel = Body(...)
    ) -> SongModel:
        song = {k: v for k, v in song.dict().items() if v is not None}

        if len(song) >= 1:
            try:
                await self.db["songs"].update_one({"_id": song_id}, {"$set": song})
                song_model = await self.get_song(song_id)
                return song_model
            except Exception as e:
                msg = f"[UPDATE_SONG] Song: {song} error: {e}"
                logging.error(msg)
                raise RuntimeError(msg)

    async def add_song(self, song: SongModel = Body(...)) -> SongModel:
        song = jsonable_encoder(song)
        await self.db["songs"].insert_one(song)
        return song

    async def list_songs_by_artist(self, artist_name: str) -> List[SongModel]:
        songs_list = []
        songs_q = self.db["songs"].find({"artists.artist_name": artist_name})
        async for song in songs_q:
            songs_list.append(SongModel(**song))
        return songs_list

    async def list_songs_by_genre(self, genre: str) -> List[SongModel]:
        songs_list = []
        songs_q = self.db["songs"].find({"genre": genre})
        async for song in songs_q:
            songs_list.append(SongModel(**song))
        return songs_list

    async def get_songs(self, list_songs):
        songs_list = []
        songs_q = self.db["songs"].find({"_id": {"$in": list_songs}})
        async for song in songs_q:
            songs_list.append(SongModel(**song))
        return songs_list
