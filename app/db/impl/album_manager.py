from typing import List

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.model.album import AlbumModel, UpdateAlbumModel, AlbumSongModel
from app.db.model.subscription import Subscription
from app.db.impl.song_manager import SongManager
from fastapi import Body
from fastapi.encoders import jsonable_encoder


class AlbumManager():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.song_manager = SongManager(self.db)

    async def with_songs(self, album: AlbumModel):
        songs_list = []
        for song_id in album["songs"]:
            song = await self.song_manager.get_song(song_id)
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
            if "songs" in album:
                list_songs = album["songs"]
                for song in list_songs:
                    await self.db["albums"].update_one(
                                                        {"_id": album_id},
                                                        {"$push": song}
                                                      )

                del album["songs"]

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
    ) -> List[AlbumSongModel]:
        albums_list = []
        albums_q = self.db["albums"].find(
            {"subscription": {"$in": Subscription.get_allowed(subscription)}}
        )
        async for album in albums_q:
            alb = await self.with_songs(album)
            albums_list.append(alb)
        return albums_list

    async def get_albums_by_genre(self, genre: str) -> List[UpdateAlbumModel]:
        albums_list = []
        albums_q = self.db["albums"].find({"genre": genre})
        async for album in albums_q:
            alb = await self.with_songs(album)
            albums_list.append(alb)
        return albums_list
