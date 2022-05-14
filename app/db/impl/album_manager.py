from typing import List
import logging

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.model.album import AlbumModel, UpdateAlbumModel, SongAlbumModel
from app.db.model.subscription import Subscription
from fastapi import Body
from fastapi.encoders import jsonable_encoder


class AlbumManager():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_albums(self) -> List[AlbumModel]:
        albums_list = []
        albums_q = self.db["albums"].find()
        async for album in albums_q:
            albums_list.append(AlbumModel(**album))
        return albums_list

    async def get_album(self, album_id: str) -> UpdateAlbumModel:
        album = await self.db["albums"].find_one({"_id": album_id})
        return album

    async def add_album(self, album: AlbumModel = Body(...)) -> AlbumModel:
        album = jsonable_encoder(album)
        await self.db["albums"].insert_one(album)
        return album

    async def update_album(
        self,
        album_id: str,
        album: UpdateAlbumModel = Body(...)
    ) -> AlbumModel:
        try:
            album = {k: v for k, v in album.dict().items() if v is not None}
            await self.db["albums"].update_one({"_id": album_id}, {"$set": album})
            album_model = await self.get_album(album_id)
            return album_model
        except Exception as e:
            msg = f"[UPDATE ALBUM] Info {album} Error: {e}"
            logging.error(msg)
            raise RuntimeError(msg)

    async def get_albums_by_artist(self, artist_id: str) -> List[AlbumModel]:
        albums_list = []
        albums_q = self.db["albums"].find({"artist": artist_id})
        async for album in albums_q:
            albums_list.append(AlbumModel(**album))
        return albums_list

    async def get_albums_by_subscription(
        self,
        subscription: str
    ) -> List[AlbumModel]:
        albums_list = []
        albums_q = self.db["albums"].find(
            {"subscription": {"$in": Subscription.get_allowed(subscription)}}
        )
        async for album in albums_q:
            albums_list.append(AlbumModel(**album))
        return albums_list

    async def get_albums_by_genre(self, genre: str) -> List[AlbumModel]:
        albums_list = []
        albums_q = self.db["albums"].find({"genre": genre})
        async for album in albums_q:
            albums_list.append(AlbumModel(**album))
        return albums_list

    async def add_song(self,
        album_id: str,
        album: SongAlbumModel = Body(...)
    ) -> AlbumModel:
        try:
            album = {k: v for k, v in album.dict().items() if v is not None}
            if "songs" in album:
                list_songs = album["songs"]
                await self.db["albums"]\
                    .update_one({"_id": album_id},
                                {"$push": {"songs": {"$each": list_songs}}}
                                )
            album_model = await self.get_album(album_id)
            return album_model
        except Exception as e:
            msg = f"[ADD SONG TO ALBUM] Info {album} Error: {e}"
            logging.error(msg)
            raise RuntimeError(msg)
