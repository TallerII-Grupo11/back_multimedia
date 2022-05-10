from typing import List

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.model.song import SongModel, UpdateSongModel
from fastapi import Body
from fastapi.encoders import jsonable_encoder


class SongManager():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

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

    async def update_song(self, song_id: str, song: UpdateSongModel = Body(...)) -> bool:
        song = {k: v for k, v in song.dict().items() if v is not None}

        if len(song) >= 1:
            try:
                await self.db["songs"].update_one({"_id": song_id}, {"$set": song})
                return True
            except:
                return False

    async def add_song(self, song: SongModel = Body(...)) -> SongModel:
        song = jsonable_encoder(song)
        await self.db["songs"].insert_one(song)
        return song

    async def list_songs_by_album(self, album_id: str = None) -> List[UpdateSongModel]:
        songs_list = []
        songs_q = self.db["songs"].find({"album_id": album_id})
        async for song in songs_q:
            songs_list.append(SongModel(**song))
        return songs_list

    async def list_songs_by_artist(self, artist: str) -> List[UpdateSongModel]:
        songs_list = []
        songs_q = self.db["songs"].find({"artists": [artist]})
        async for song in songs_q:
            songs_list.append(SongModel(**song))
        return songs_list
